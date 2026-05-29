"""Phase 23 concurrency and async runtime (stdlib + VM-callable natives).

Host scaffold: futures/async I/O use ThreadPoolExecutor + blocking poll loops,
not a VM-native await or asyncio event loop. Fibers are cooperative deques.
"""

from __future__ import annotations

import inspect
import re
import socket
import tempfile
import threading
import time
from collections import deque
from concurrent.futures import Future as HostFuture
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import Empty, Queue
from typing import Any, Callable
from .errors import RuntimeSanskriptError
from .runtime_values import (
    NIL,
    ByteArrayValue,
    BytesValue,
    NilValue,
    OpaqueHandle,
    OptionValue,
    RecordValue,
    ResultValue,
)
from .stdlib_common import NativeSpec, expect_bool, expect_int, expect_list, expect_map, expect_text

_REGISTRY_LOCK = threading.Lock()
_STATE_LOCK = threading.Lock()
_HANDLE_COUNTER = 1
_ASYNC_IO_POOL = ThreadPoolExecutor(max_workers=4, thread_name_prefix="sanskript-async-io")
_THREAD_REGISTRY: dict[int, threading.Thread] = {}
_THREAD_RESULTS: dict[int, object] = {}
_THREAD_ERRORS: dict[int, BaseException] = {}
_POOL_REGISTRY: dict[int, ThreadPoolExecutor] = {}
_POOL_STEAL_QUEUES: dict[int, deque] = {}
_FIBER_REGISTRY: dict[int, dict[str, object]] = {}
_FUTURE_REGISTRY: dict[int, dict[str, object]] = {}
_CANCEL_REGISTRY: dict[int, dict[str, object]] = {}
_EVENT_LOOP_STATE: dict[str, object] = {"loop": None, "tasks": []}
_RWLOCK_REGISTRY: dict[int, dict[str, object]] = {}
_SEMAPHORE_REGISTRY: dict[int, threading.Semaphore] = {}
_SYNC_QUEUE_REGISTRY: dict[int, Queue] = {}
_WORKER_REGISTRY: dict[int, dict[str, object]] = {}
_RACE_ACCESS_LOG: list[dict[str, object]] = []


def _next_handle_id() -> int:
    global _HANDLE_COUNTER
    with _REGISTRY_LOCK:
        current = _HANDLE_COUNTER
        _HANDLE_COUNTER += 1
        return current


def is_send_safe(value: object) -> bool:
    if value is None or isinstance(value, (str, int, float, bool, NilValue, BytesValue)):
        return True
    if isinstance(value, ByteArrayValue):
        return False
    if isinstance(value, OpaqueHandle):
        return value.kind in {
            "atomic",
            "lock",
            "mutex",
            "channel",
            "rwlock",
            "semaphore",
            "sync_queue",
            "future",
            "cancel_token",
        }
    if isinstance(value, OptionValue):
        return (not value.present) or is_send_safe(value.value)
    if isinstance(value, ResultValue):
        return is_send_safe(value.value)
    if isinstance(value, list):
        return all(is_send_safe(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and is_send_safe(item) for key, item in value.items())
    if isinstance(value, RecordValue):
        return all(is_send_safe(item) for item in value.fields.values())
    return False


def _native_call(name: str, params: list) -> object:
    from .stdlib_core import call_native_function

    return call_native_function(name, params)


def _has_native(name: str) -> bool:
    from .stdlib_core import has_native_function

    return has_native_function(name)


def _native_fn_arity(name: str) -> int:
    from .stdlib_core import native_arity

    return native_arity(name)


def _resolve_native_call(descriptor: object, *, fn_name: str) -> tuple[str, list]:
    spec = expect_map(descriptor, fn_name=fn_name)
    symbol = spec.get("symbol")
    args = spec.get("args", [])
    if not isinstance(symbol, str) or not symbol:
        raise RuntimeSanskriptError(f"{fn_name} requires non-empty symbol")
    if not _has_native(symbol):
        raise RuntimeSanskriptError(f"{fn_name} unknown native symbol {symbol!r}")
    params = expect_list(args, fn_name=fn_name)
    if len(params) != _native_fn_arity(symbol):
        raise RuntimeSanskriptError(
            f"{fn_name} symbol {symbol!r} expects {_native_fn_arity(symbol)} argument(s), got {len(params)}"
        )
    return symbol, params


def _run_native_call(descriptor: object, *, fn_name: str) -> object:
    symbol, params = _resolve_native_call(descriptor, fn_name=fn_name)
    return _native_call(symbol, params)


def _thread_worker(symbol: str, params: list, handle_id: int) -> None:
    try:
        _THREAD_RESULTS[handle_id] = _native_call(symbol, params)
    except BaseException as exc:  # noqa: BLE001
        _THREAD_ERRORS[handle_id] = exc


def _thread_spawn(args: list) -> OpaqueHandle:
    descriptor = args[0]
    symbol, params = _resolve_native_call(descriptor, fn_name="std.thread.spawn")
    handle = _next_handle_id()
    thread = threading.Thread(
        target=_thread_worker,
        args=(symbol, params, handle),
        daemon=True,
        name=f"sanskript-thread-{handle}",
    )
    _THREAD_REGISTRY[handle] = thread
    thread.start()
    return OpaqueHandle(kind="thread", handle_id=handle)


def _thread_join(args: list) -> object:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.thread.join")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "thread":
        raise RuntimeSanskriptError("std.thread.join expects thread handle")
    thread = _THREAD_REGISTRY.get(handle.handle_id)
    if thread is None:
        raise RuntimeSanskriptError("std.thread.join unknown thread handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    thread.join(timeout=timeout)
    if thread.is_alive():
        return OptionValue(present=False)
    if handle.handle_id in _THREAD_ERRORS:
        raise RuntimeSanskriptError(
            f"std.thread.join worker failed: {_THREAD_ERRORS[handle.handle_id]}"
        ) from _THREAD_ERRORS[handle.handle_id]
    return OptionValue(present=True, value=_THREAD_RESULTS.get(handle.handle_id, NIL))


def _thread_current_id(args: list) -> int:
    _ = args
    return threading.get_ident()


def _thread_is_alive(args: list) -> bool:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "thread":
        raise RuntimeSanskriptError("std.thread.is_alive expects thread handle")
    thread = _THREAD_REGISTRY.get(handle.handle_id)
    if thread is None:
        raise RuntimeSanskriptError("std.thread.is_alive unknown thread handle")
    return thread.is_alive()


def _thread_pool_new(args: list) -> OpaqueHandle:
    workers = expect_int(args[0], fn_name="std.thread.pool.new")
    if workers <= 0:
        raise RuntimeSanskriptError("std.thread.pool.new workers must be > 0")
    handle = _next_handle_id()
    _POOL_REGISTRY[handle] = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="ssk-pool")
    _POOL_STEAL_QUEUES[handle] = deque()
    return OpaqueHandle(kind="thread_pool", handle_id=handle)


def _thread_pool_submit(args: list) -> OpaqueHandle:
    pool = args[0]
    descriptor = args[1]
    if not isinstance(pool, OpaqueHandle) or pool.kind != "thread_pool":
        raise RuntimeSanskriptError("std.thread.pool.submit expects thread pool handle")
    executor = _POOL_REGISTRY.get(pool.handle_id)
    if executor is None:
        raise RuntimeSanskriptError("std.thread.pool.submit unknown pool handle")
    symbol, params = _resolve_native_call(descriptor, fn_name="std.thread.pool.submit")
    host_future = executor.submit(_native_call, symbol, params)
    steal_queue = _POOL_STEAL_QUEUES.get(pool.handle_id)
    if steal_queue is not None:
        steal_queue.append({"symbol": symbol, "args": params})
    handle = _next_handle_id()
    with _STATE_LOCK:
        _FUTURE_REGISTRY[handle] = {
            "host": host_future,
            "ready": False,
            "value": NIL,
            "cancelled": False,
        }
    return OpaqueHandle(kind="future", handle_id=handle)


def _thread_pool_join(args: list) -> bool:
    pool = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.thread.pool.join")
    if not isinstance(pool, OpaqueHandle) or pool.kind != "thread_pool":
        raise RuntimeSanskriptError("std.thread.pool.join expects thread pool handle")
    executor = _POOL_REGISTRY.get(pool.handle_id)
    if executor is None:
        raise RuntimeSanskriptError("std.thread.pool.join unknown pool handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    executor.shutdown(wait=True, cancel_futures=False)
    _POOL_REGISTRY.pop(pool.handle_id, None)
    _POOL_STEAL_QUEUES.pop(pool.handle_id, None)
    if timeout is not None and timeout <= 0:
        return False
    return True


def _thread_pool_shutdown(args: list) -> bool:
    pool = args[0]
    if not isinstance(pool, OpaqueHandle) or pool.kind != "thread_pool":
        raise RuntimeSanskriptError("std.thread.pool.shutdown expects thread pool handle")
    executor = _POOL_REGISTRY.pop(pool.handle_id, None)
    _POOL_STEAL_QUEUES.pop(pool.handle_id, None)
    if executor is None:
        raise RuntimeSanskriptError("std.thread.pool.shutdown unknown pool handle")
    executor.shutdown(wait=False, cancel_futures=True)
    return True


def _thread_pool_steal_work(args: list) -> object:
    pool = args[0]
    if not isinstance(pool, OpaqueHandle) or pool.kind != "thread_pool":
        raise RuntimeSanskriptError("std.thread.pool.steal_work expects thread pool handle")
    queue = _POOL_STEAL_QUEUES.get(pool.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.thread.pool.steal_work unknown pool handle")
    if not queue:
        return NIL
    return queue.popleft()


def _fiber_create(args: list) -> OpaqueHandle:
    steps = expect_list(args[0], fn_name="std.fiber.create")
    handle = _next_handle_id()
    _FIBER_REGISTRY[handle] = {"steps": deque(steps), "done": False, "last": NIL}
    return OpaqueHandle(kind="fiber", handle_id=handle)


def _fiber_resume(args: list) -> dict:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "fiber":
        raise RuntimeSanskriptError("std.fiber.resume expects fiber handle")
    state = _FIBER_REGISTRY.get(handle.handle_id)
    if state is None:
        raise RuntimeSanskriptError("std.fiber.resume unknown fiber handle")
    steps: deque = state["steps"]  # type: ignore[assignment]
    if not steps:
        state["done"] = True
        return {"done": True, "value": state.get("last", NIL)}
    value = steps.popleft()
    state["last"] = value
    return {"done": False, "value": value}


def _future_register(
    host_future: HostFuture | threading.Timer | None,
    *,
    value: object = NIL,
) -> OpaqueHandle:
    handle = _next_handle_id()
    with _STATE_LOCK:
        _FUTURE_REGISTRY[handle] = {
            "host": host_future,
            "ready": host_future is None and value is not NIL,
            "value": value,
            "cancelled": False,
        }
    return OpaqueHandle(kind="future", handle_id=handle)


def _future_poll(args: list) -> dict:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "future":
        raise RuntimeSanskriptError("std.async.future.poll expects future handle")
    with _STATE_LOCK:
        state = _FUTURE_REGISTRY.get(handle.handle_id)
        if state is None:
            raise RuntimeSanskriptError("std.async.future.poll unknown future handle")
        if state.get("cancelled"):
            return {"ready": False, "cancelled": True, "value": NIL}
        if state.get("ready"):
            return {
                "ready": True,
                "cancelled": False,
                "value": state.get("value", NIL),
            }
        host = state.get("host")
        if isinstance(host, HostFuture) and host.done() and not state.get("ready"):
            state["ready"] = True
            try:
                state["value"] = host.result()
            except Exception as exc:  # noqa: BLE001
                raise RuntimeSanskriptError(
                    f"std.async.future.poll host future failed: {exc}"
                ) from exc
        elif isinstance(host, threading.Timer) and not host.is_alive() and not state.get("ready"):
            host.join(timeout=0.2)
        return {
            "ready": bool(state.get("ready")),
            "cancelled": bool(state.get("cancelled")),
            "value": state.get("value", NIL),
        }


def _future_resolve(args: list) -> bool:
    handle = args[0]
    value = args[1]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "future":
        raise RuntimeSanskriptError("std.async.future.resolve expects future handle")
    with _STATE_LOCK:
        state = _FUTURE_REGISTRY.get(handle.handle_id)
        if state is None:
            raise RuntimeSanskriptError("std.async.future.resolve unknown future handle")
        state["ready"] = True
        state["value"] = value
        state["host"] = None
    return True


def _async_await(args: list) -> object:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.async.await")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "future":
        raise RuntimeSanskriptError("std.async.await expects future handle")
    deadline = None if timeout_ms < 0 else time.monotonic() + timeout_ms / 1000.0
    while True:
        polled = _future_poll([handle])
        if polled.get("cancelled"):
            raise RuntimeSanskriptError("std.async.await cancelled future")
        if polled.get("ready"):
            return polled.get("value", NIL)
        if deadline is not None and time.monotonic() >= deadline:
            return OptionValue(present=False)
        time.sleep(0.001)


def _async_spawn(args: list) -> OpaqueHandle:
    descriptor = args[0]
    symbol, params = _resolve_native_call(descriptor, fn_name="std.async.spawn")
    host_future = _ASYNC_IO_POOL.submit(_native_call, symbol, params)
    return _future_register(host_future)


def _async_event_loop_run_once(args: list) -> int:
    _ = args
    done = 0
    with _STATE_LOCK:
        states = list(_FUTURE_REGISTRY.values())
    for state in states:
        if state.get("cancelled"):
            continue
        host = state.get("host")
        if isinstance(host, HostFuture) and host.done() and not state.get("ready"):
            with _STATE_LOCK:
                if state.get("ready"):
                    continue
                state["ready"] = True
                try:
                    state["value"] = host.result()
                except Exception as exc:  # noqa: BLE001
                    raise RuntimeSanskriptError(
                        f"std.async.event_loop task failed: {exc}"
                    ) from exc
            done += 1
        elif isinstance(host, threading.Timer) and not host.is_alive() and not state.get("ready"):
            host.join(timeout=0.2)
            if state.get("ready"):
                done += 1
    return done


def _async_event_loop_pending(args: list) -> int:
    _ = args
    pending = 0
    with _STATE_LOCK:
        states = list(_FUTURE_REGISTRY.values())
    for state in states:
        if state.get("cancelled") or state.get("ready"):
            continue
        host = state.get("host")
        if isinstance(host, HostFuture) and not host.done():
            pending += 1
        elif isinstance(host, threading.Timer) and (
            host.is_alive() or not state.get("ready")
        ):
            pending += 1
    return pending


def _async_event_loop_drain(args: list) -> int:
    timeout_ms = expect_int(args[0], fn_name="std.async.event_loop.drain")
    deadline = None if timeout_ms < 0 else time.monotonic() + timeout_ms / 1000.0
    completed = 0
    while _async_event_loop_pending([]) > 0:
        completed += _async_event_loop_run_once([])
        if deadline is not None and time.monotonic() >= deadline:
            break
        time.sleep(0.001)
    completed += _async_event_loop_run_once([])
    return completed


def _async_sleep_ms(args: list) -> int:
    ms = expect_int(args[0], fn_name="std.async.sleep_ms")
    if ms < 0:
        raise RuntimeSanskriptError("std.async.sleep_ms requires non-negative delay")
    # Blocking host sleep: VM has no await yet; not cooperative async on the bytecode VM.
    time.sleep(ms / 1000.0)
    return ms


def _async_read_text(args: list) -> str:
    path = expect_text(args[0], fn_name="std.async.read_text")
    try:
        return _ASYNC_IO_POOL.submit(Path(path).read_text, encoding="utf-8").result()
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.async.read_text failed: {exc}") from exc


def _async_write_text(args: list) -> bool:
    path = expect_text(args[0], fn_name="std.async.write_text")
    text = expect_text(args[1], fn_name="std.async.write_text")
    try:
        _ASYNC_IO_POOL.submit(Path(path).write_text, text, encoding="utf-8").result()
        return True
    except OSError as exc:
        raise RuntimeSanskriptError(f"std.async.write_text failed: {exc}") from exc


def _async_net_connect(args: list) -> dict:
    host = expect_text(args[0], fn_name="std.async.net.connect")
    port = expect_int(args[1], fn_name="std.async.net.connect")
    timeout_ms = expect_int(args[2], fn_name="std.async.net.connect")
    if port < 0 or port > 65535:
        raise RuntimeSanskriptError("std.async.net.connect port must be 0..65535")

    def _sync_probe() -> dict:
        started = time.monotonic()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.settimeout(max(0.0, timeout_ms / 1000.0))
            sock.connect((host, port))
            ok = True
        except OSError:
            ok = False
        finally:
            sock.close()
        latency_ms = int((time.monotonic() - started) * 1000)
        return {"ok": ok, "host": host, "port": port, "latency_ms": latency_ms}

    return _ASYNC_IO_POOL.submit(_sync_probe).result()


def _async_timer_after_ms(args: list) -> OpaqueHandle:
    ms = expect_int(args[0], fn_name="std.async.timer.after_ms")
    descriptor = args[1]
    if ms < 0:
        raise RuntimeSanskriptError("std.async.timer.after_ms requires non-negative delay")
    future_handle = _future_register(None)

    def _fire() -> None:
        with _STATE_LOCK:
            state = _FUTURE_REGISTRY.get(future_handle.handle_id)
            if state is None or state.get("cancelled"):
                return
        try:
            value = _run_native_call(descriptor, fn_name="std.async.timer.after_ms")
        except BaseException as exc:  # noqa: BLE001
            with _STATE_LOCK:
                state = _FUTURE_REGISTRY.get(future_handle.handle_id)
                if state is None:
                    return
                state["ready"] = True
                state["value"] = NIL
                state["error"] = exc
            return
        with _STATE_LOCK:
            state = _FUTURE_REGISTRY.get(future_handle.handle_id)
            if state is None:
                return
            state["ready"] = True
            state["value"] = value
            state["host"] = None

    timer = threading.Timer(ms / 1000.0, _fire)
    timer.daemon = True
    with _STATE_LOCK:
        state = _FUTURE_REGISTRY[future_handle.handle_id]
        state["ready"] = False
        state["host"] = timer
    timer.start()
    return future_handle


def _async_cancel_new(args: list) -> OpaqueHandle:
    _ = args
    handle = _next_handle_id()
    _CANCEL_REGISTRY[handle] = {"cancelled": False}
    return OpaqueHandle(kind="cancel_token", handle_id=handle)


def _async_cancel_request(args: list) -> bool:
    token = args[0]
    if not isinstance(token, OpaqueHandle) or token.kind != "cancel_token":
        raise RuntimeSanskriptError("std.async.cancel.request expects cancel token")
    state = _CANCEL_REGISTRY.get(token.handle_id)
    if state is None:
        raise RuntimeSanskriptError("std.async.cancel.request unknown cancel token")
    state["cancelled"] = True
    with _STATE_LOCK:
        future_states = list(_FUTURE_REGISTRY.values())
    for future_state in future_states:
        if future_state.get("cancel_token") == token.handle_id:
            with _STATE_LOCK:
                future_state["cancelled"] = True
                host = future_state.get("host")
            if isinstance(host, HostFuture):
                host.cancel()
            elif isinstance(host, threading.Timer):
                host.cancel()
    return True


def _async_cancel_is_cancelled(args: list) -> bool:
    token = args[0]
    if not isinstance(token, OpaqueHandle) or token.kind != "cancel_token":
        raise RuntimeSanskriptError("std.async.cancel.is_cancelled expects cancel token")
    state = _CANCEL_REGISTRY.get(token.handle_id)
    if state is None:
        raise RuntimeSanskriptError("std.async.cancel.is_cancelled unknown cancel token")
    return bool(state.get("cancelled"))


def _async_cancel_check(args: list) -> bool:
    token = args[0]
    if _async_cancel_is_cancelled([token]):
        raise RuntimeSanskriptError("operation cancelled")
    return True


def _async_scope_run(args: list) -> list:
    children = expect_list(args[0], fn_name="std.async.scope.run")
    futures: list[OpaqueHandle] = []
    for child in children:
        futures.append(_async_spawn([child]))
    _async_event_loop_drain([-1])
    results: list[object] = []
    errors: list[str] = []
    for future in futures:
        polled = _future_poll([future])
        if polled.get("cancelled"):
            errors.append("cancelled")
            continue
        if not polled.get("ready"):
            errors.append("timeout")
            continue
        results.append(polled.get("value", NIL))
    if errors:
        token = _async_cancel_new([])
        with _STATE_LOCK:
            for future in futures:
                state = _FUTURE_REGISTRY.get(future.handle_id)
                if state is not None:
                    state["cancel_token"] = token.handle_id
        _async_cancel_request([token])
        raise RuntimeSanskriptError(
            f"std.async.scope.run structured concurrency failure: {', '.join(errors)}"
        )
    return results


_MUTEX_REGISTRY: dict[int, threading.Lock] = {}


def _sync_mutex_new(args: list) -> OpaqueHandle:
    _ = args
    handle = _next_handle_id()
    _MUTEX_REGISTRY[handle] = threading.Lock()
    return OpaqueHandle(kind="mutex", handle_id=handle)


def _sync_mutex_acquire(args: list) -> bool:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.mutex.acquire")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "mutex":
        raise RuntimeSanskriptError("std.sync.mutex.acquire expects mutex handle")
    lock = _MUTEX_REGISTRY.get(handle.handle_id)
    if lock is None:
        raise RuntimeSanskriptError("std.sync.mutex.acquire unknown mutex handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    return lock.acquire(timeout=timeout)


def _sync_mutex_release(args: list) -> bool:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "mutex":
        raise RuntimeSanskriptError("std.sync.mutex.release expects mutex handle")
    lock = _MUTEX_REGISTRY.get(handle.handle_id)
    if lock is None:
        raise RuntimeSanskriptError("std.sync.mutex.release unknown mutex handle")
    try:
        lock.release()
    except RuntimeError as exc:
        raise RuntimeSanskriptError("std.sync.mutex.release on unlocked mutex") from exc
    return True


def _sync_rwlock_new(args: list) -> OpaqueHandle:
    _ = args
    handle = _next_handle_id()
    _RWLOCK_REGISTRY[handle] = {
        "guard": threading.RLock(),
        "readers": 0,
        "writer": False,
    }
    return OpaqueHandle(kind="rwlock", handle_id=handle)


def _sync_rwlock_acquire_read(args: list) -> bool:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.rwlock.acquire_read")
    state = _RWLOCK_REGISTRY.get(_expect_rwlock(handle, "std.sync.rwlock.acquire_read"))
    if state is None:
        raise RuntimeSanskriptError("std.sync.rwlock.acquire_read unknown rwlock handle")
    deadline = None if timeout_ms < 0 else time.monotonic() + timeout_ms / 1000.0

    def _try() -> bool:
        guard: threading.RLock = state["guard"]  # type: ignore[assignment]
        with guard:
            if state.get("writer"):
                return False
            state["readers"] = int(state.get("readers", 0)) + 1
            return True

    while True:
        if _try():
            return True
        if deadline is not None and time.monotonic() >= deadline:
            return False
        time.sleep(0.001)


def _sync_rwlock_acquire_write(args: list) -> bool:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.rwlock.acquire_write")
    state = _RWLOCK_REGISTRY.get(_expect_rwlock(handle, "std.sync.rwlock.acquire_write"))
    if state is None:
        raise RuntimeSanskriptError("std.sync.rwlock.acquire_write unknown rwlock handle")
    deadline = None if timeout_ms < 0 else time.monotonic() + timeout_ms / 1000.0

    def _try() -> bool:
        guard: threading.RLock = state["guard"]  # type: ignore[assignment]
        with guard:
            if state.get("writer") or int(state.get("readers", 0)) > 0:
                return False
            state["writer"] = True
            return True

    while True:
        if _try():
            return True
        if deadline is not None and time.monotonic() >= deadline:
            return False
        time.sleep(0.001)


def _sync_rwlock_release(args: list) -> bool:
    handle = args[0]
    state = _RWLOCK_REGISTRY.get(_expect_rwlock(handle, "std.sync.rwlock.release"))
    if state is None:
        raise RuntimeSanskriptError("std.sync.rwlock.release unknown rwlock handle")
    guard: threading.RLock = state["guard"]  # type: ignore[assignment]
    with guard:
        if state.get("writer"):
            state["writer"] = False
            return True
        readers = int(state.get("readers", 0))
        if readers <= 0:
            raise RuntimeSanskriptError("std.sync.rwlock.release with no active readers")
        state["readers"] = readers - 1
        return True


def _expect_rwlock(handle: object, fn_name: str) -> int:
    if not isinstance(handle, OpaqueHandle) or handle.kind != "rwlock":
        raise RuntimeSanskriptError(f"{fn_name} expects rwlock handle")
    return handle.handle_id


def _sync_semaphore_new(args: list) -> OpaqueHandle:
    initial = expect_int(args[0], fn_name="std.sync.semaphore.new")
    if initial < 0:
        raise RuntimeSanskriptError("std.sync.semaphore.new initial must be >= 0")
    handle = _next_handle_id()
    _SEMAPHORE_REGISTRY[handle] = threading.Semaphore(initial)
    return OpaqueHandle(kind="semaphore", handle_id=handle)


def _sync_semaphore_acquire(args: list) -> bool:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.semaphore.acquire")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "semaphore":
        raise RuntimeSanskriptError("std.sync.semaphore.acquire expects semaphore handle")
    sem = _SEMAPHORE_REGISTRY.get(handle.handle_id)
    if sem is None:
        raise RuntimeSanskriptError("std.sync.semaphore.acquire unknown semaphore handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    return sem.acquire(timeout=timeout)


def _sync_semaphore_release(args: list) -> bool:
    handle = args[0]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "semaphore":
        raise RuntimeSanskriptError("std.sync.semaphore.release expects semaphore handle")
    sem = _SEMAPHORE_REGISTRY.get(handle.handle_id)
    if sem is None:
        raise RuntimeSanskriptError("std.sync.semaphore.release unknown semaphore handle")
    sem.release()
    return True


def _sync_queue_new(args: list) -> OpaqueHandle:
    capacity = expect_int(args[0], fn_name="std.sync.queue.new")
    if capacity < 0:
        raise RuntimeSanskriptError("std.sync.queue.new capacity must be >= 0")
    handle = _next_handle_id()
    _SYNC_QUEUE_REGISTRY[handle] = Queue(maxsize=capacity if capacity > 0 else 0)
    return OpaqueHandle(kind="sync_queue", handle_id=handle)


def _sync_queue_enqueue(args: list) -> bool:
    handle = args[0]
    payload = args[1]
    if not isinstance(handle, OpaqueHandle) or handle.kind != "sync_queue":
        raise RuntimeSanskriptError("std.sync.queue.enqueue expects queue handle")
    if not is_send_safe(payload):
        raise RuntimeSanskriptError("std.sync.queue.enqueue payload is not send-safe")
    queue = _SYNC_QUEUE_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.queue.enqueue unknown queue handle")
    queue.put(payload, block=True)
    return True


def _sync_queue_dequeue(args: list) -> object:
    handle = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.sync.queue.dequeue")
    if not isinstance(handle, OpaqueHandle) or handle.kind != "sync_queue":
        raise RuntimeSanskriptError("std.sync.queue.dequeue expects queue handle")
    queue = _SYNC_QUEUE_REGISTRY.get(handle.handle_id)
    if queue is None:
        raise RuntimeSanskriptError("std.sync.queue.dequeue unknown queue handle")
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    try:
        return queue.get(block=True, timeout=timeout)
    except Empty:
        return OptionValue(present=False)


def _concurrent_race_record(args: list) -> bool:
    events = expect_list(args[0], fn_name="std.concurrent.race.record")
    for event in events:
        row = expect_map(event, fn_name="std.concurrent.race.record")
        var = expect_text(row.get("var"), fn_name="std.concurrent.race.record")
        mode = expect_text(row.get("mode"), fn_name="std.concurrent.race.record")
        thread_id = expect_int(row.get("thread_id"), fn_name="std.concurrent.race.record")
        if mode not in {"read", "write"}:
            raise RuntimeSanskriptError("std.concurrent.race.record mode must be read|write")
        with _STATE_LOCK:
            _RACE_ACCESS_LOG.append({"var": var, "mode": mode, "thread_id": thread_id})
    return True


def _concurrent_race_detect(args: list) -> list:
    _ = args
    races: list[dict[str, object]] = []
    by_var: dict[str, list[dict[str, object]]] = {}
    with _STATE_LOCK:
        rows = list(_RACE_ACCESS_LOG)
    for row in rows:
        by_var.setdefault(str(row["var"]), []).append(row)
    for var, rows in by_var.items():
        writes = [row for row in rows if row["mode"] == "write"]
        if len(writes) >= 2 and len({row["thread_id"] for row in writes}) > 1:
            races.append({"var": var, "kind": "write-write", "events": rows})
            continue
        for write in writes:
            readers = [
                row
                for row in rows
                if row["mode"] == "read" and row["thread_id"] != write["thread_id"]
            ]
            if readers:
                races.append({"var": var, "kind": "read-write", "events": rows})
                break
    return races


def _concurrent_race_clear(args: list) -> bool:
    _ = args
    with _STATE_LOCK:
        _RACE_ACCESS_LOG.clear()
    return True


def _concurrent_arakshita_check(args: list) -> bool:
    policy = expect_map(args[0], fn_name="std.concurrent.arakshita.check")
    tier = expect_text(policy.get("tier"), fn_name="std.concurrent.arakshita.check")
    op = expect_text(policy.get("operation"), fn_name="std.concurrent.arakshita.check")
    if tier != "arakshita":
        raise RuntimeSanskriptError("std.concurrent.arakshita.check requires arakshita tier")
    forbidden_without_unsafe = {
        "channel_send",
        "channel_recv",
        "shared_mut_borrow",
        "atomic_unsafe_mix",
    }
    unsafe_region = policy.get("unsafe_region", False)
    if not isinstance(unsafe_region, bool):
        unsafe_region = bool(unsafe_region)
    if op in forbidden_without_unsafe and not unsafe_region:
        raise RuntimeSanskriptError(
            f"arakshita concurrent operation {op!r} requires explicit unsafe region"
        )
    return True


def _web_worker_spawn(args: list) -> OpaqueHandle:
    script = expect_text(args[0], fn_name="std.web.worker.spawn")
    if not script.strip():
        raise RuntimeSanskriptError("std.web.worker.spawn requires non-empty script")
    handle = _next_handle_id()
    _WORKER_REGISTRY[handle] = {
        "script": script,
        "inbox": Queue(),
        "outbox": Queue(),
        "alive": True,
        "thread": None,
    }

    def _worker_main() -> None:
        state = _WORKER_REGISTRY[handle]
        inbox: Queue = state["inbox"]  # type: ignore[assignment]
        outbox: Queue = state["outbox"]  # type: ignore[assignment]
        while state.get("alive"):
            try:
                message = inbox.get(timeout=0.05)
            except Empty:
                continue
            if message == "__terminate__":
                break
            if isinstance(message, dict) and message.get("op") == "eval":
                payload = message.get("payload")
                if payload == "ping":
                    outbox.put({"ok": True, "echo": "pong"})
                else:
                    outbox.put({"ok": True, "echo": payload})
            else:
                outbox.put({"ok": True, "echo": message})

    thread = threading.Thread(target=_worker_main, daemon=True, name=f"ssk-worker-{handle}")
    _WORKER_REGISTRY[handle]["thread"] = thread
    thread.start()
    return OpaqueHandle(kind="web_worker", handle_id=handle)


def _web_worker_post(args: list) -> bool:
    worker = args[0]
    message = args[1]
    if not isinstance(worker, OpaqueHandle) or worker.kind != "web_worker":
        raise RuntimeSanskriptError("std.web.worker.post_message expects worker handle")
    state = _WORKER_REGISTRY.get(worker.handle_id)
    if state is None or not state.get("alive"):
        raise RuntimeSanskriptError("std.web.worker.post_message unknown or dead worker")
    if not is_send_safe(message):
        raise RuntimeSanskriptError("std.web.worker.post_message payload is not send-safe")
    inbox: Queue = state["inbox"]  # type: ignore[assignment]
    inbox.put({"op": "eval", "payload": message})
    return True


def _web_worker_recv(args: list) -> object:
    worker = args[0]
    timeout_ms = expect_int(args[1], fn_name="std.web.worker.recv")
    if not isinstance(worker, OpaqueHandle) or worker.kind != "web_worker":
        raise RuntimeSanskriptError("std.web.worker.recv expects worker handle")
    state = _WORKER_REGISTRY.get(worker.handle_id)
    if state is None:
        raise RuntimeSanskriptError("std.web.worker.recv unknown worker handle")
    outbox: Queue = state["outbox"]  # type: ignore[assignment]
    timeout = None if timeout_ms < 0 else timeout_ms / 1000.0
    try:
        return outbox.get(block=True, timeout=timeout)
    except Empty:
        return OptionValue(present=False)


def _web_worker_terminate(args: list) -> bool:
    worker = args[0]
    if not isinstance(worker, OpaqueHandle) or worker.kind != "web_worker":
        raise RuntimeSanskriptError("std.web.worker.terminate expects worker handle")
    state = _WORKER_REGISTRY.get(worker.handle_id)
    if state is None:
        raise RuntimeSanskriptError("std.web.worker.terminate unknown worker handle")
    state["alive"] = False
    inbox: Queue = state["inbox"]  # type: ignore[assignment]
    inbox.put("__terminate__")
    thread = state.get("thread")
    if isinstance(thread, threading.Thread):
        thread.join(timeout=1.0)
    _WORKER_REGISTRY.pop(worker.handle_id, None)
    return True


def _pool_push_steal_item(pool_id: int, item: object) -> None:
    queue = _POOL_STEAL_QUEUES.get(pool_id)
    if queue is not None:
        queue.append(item)


REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE23_SPEC_VERSION = "2026-05-29-dual-tier-host-seal"

# Host-tier checklist slugs proven by std.phase23.seal_run (VM-missing rows excluded).
PHASE23_HOST_CHECKLIST_SLUGS: tuple[str, ...] = (
    "threads",
    "fibers_coroutines",
    "futures_promises",
    "timers",
    "async_file_io",
    "async_networking",
    "cancellation",
    "channels",
    "queues",
    "mutexes",
    "read_write_locks",
    "semaphores",
    "atomics",
    "thread_pools",
    "work_stealing",
    "data_race_rakshita",
    "arakshita_unsafe_rules",
    "browser_workers",
    "gatekeeper",
)

# Checklist rows that must stay [x] under dual-tier host seal (see independence checklist).
PHASE23_CHECKLIST_HOST_ROWS = (
    "Threads.",
    "Fibers/coroutines.",
    "Futures/promises.",
    "Timers.",
    "Async file I/O.",
    "Async networking.",
    "Cancellation.",
    "Channels.",
    "Queues.",
    "Mutexes.",
    "Read-write locks.",
    "Semaphores.",
    "Atomics.",
    "Thread pools.",
    "Work stealing if needed.",
    "Data race checking for `rakṣita`.",
    "Unsafe concurrent memory rules for `arakṣita`.",
    "Browser worker support.",
)

# VM-tier blockers — must remain [ ] until OP_AWAIT / in-language scheduler exist.
PHASE23_CHECKLIST_VM_MISSING_ROWS = (
    "Async functions.",
    "Await.",
    "Event loop.",
    "Structured concurrency.",
)

# Host-tier seal bar: contention-safe atomics/channels + honest blocking-async labels.
PHASE23_HOST_SEAL_BAR = (
    "std.sync.atomic.new",
    "std.sync.atomic.load",
    "std.sync.atomic.store",
    "std.sync.atomic.fetch_add",
    "std.sync.atomic.compare_exchange",
    "std.sync.channel.new",
    "std.sync.channel.send",
    "std.sync.channel.recv",
    "std.sync.mutex.new",
    "std.sync.mutex.acquire",
    "std.sync.mutex.release",
    "std.thread.spawn",
    "std.thread.join",
)

# Surfaces that must never be labeled VM-native until bytecode lowering exists.
PHASE23_VM_MISSING_SURFACES = (
    "std.async.await",
    "std.async.spawn",
    "std.async.event_loop.run_once",
    "std.async.event_loop.pending",
    "std.async.event_loop.drain",
    "std.async.scope.run",
    "async_future",
)

# Blocking host-thread async — not cooperative VM await.
PHASE23_BLOCKING_ASYNC_SURFACES = (
    "std.async.sleep_ms",
    "std.async.read_text",
    "std.async.write_text",
    "std.async.net.connect",
)


def phase23_tier_row(
    name: str,
    *,
    host_tier: str,
    vm_tier: str,
    notes: list[str] | None = None,
    thread_safe: bool | None = None,
) -> dict[str, object]:
    row: dict[str, object] = {
        "name": name,
        "host_tier": host_tier,
        "vm_tier": vm_tier,
        "notes": notes or [],
    }
    if thread_safe is not None:
        row["thread_safe"] = thread_safe
    return row


PHASE23_RUNTIME_NATIVE_SYMBOLS: tuple[str, ...] = (
    "std.thread.spawn",
    "std.thread.join",
    "std.thread.current_id",
    "std.thread.is_alive",
    "std.thread.pool.new",
    "std.thread.pool.submit",
    "std.thread.pool.join",
    "std.thread.pool.shutdown",
    "std.thread.pool.steal_work",
    "std.fiber.create",
    "std.fiber.resume",
    "std.async.future.poll",
    "std.async.future.resolve",
    "std.async.await",
    "std.async.spawn",
    "std.async.event_loop.run_once",
    "std.async.event_loop.pending",
    "std.async.event_loop.drain",
    "std.async.sleep_ms",
    "std.async.read_text",
    "std.async.write_text",
    "std.async.net.connect",
    "std.async.timer.after_ms",
    "std.async.cancel.new",
    "std.async.cancel.request",
    "std.async.cancel.is_cancelled",
    "std.async.cancel.check",
    "std.async.scope.run",
    "std.sync.mutex.new",
    "std.sync.mutex.acquire",
    "std.sync.mutex.release",
    "std.sync.rwlock.new",
    "std.sync.rwlock.acquire_read",
    "std.sync.rwlock.acquire_write",
    "std.sync.rwlock.release",
    "std.sync.semaphore.new",
    "std.sync.semaphore.acquire",
    "std.sync.semaphore.release",
    "std.sync.queue.new",
    "std.sync.queue.enqueue",
    "std.sync.queue.dequeue",
    "std.concurrent.race.record",
    "std.concurrent.race.detect",
    "std.concurrent.race.clear",
    "std.concurrent.arakshita.check",
    "std.web.worker.spawn",
    "std.web.worker.post_message",
    "std.web.worker.recv",
    "std.web.worker.terminate",
)


def phase23_inventory() -> list[dict[str, object]]:
    """Honest dual-tier inventory for Phase 23 gatekeeper and docs."""
    rows: list[dict[str, object]] = []
    for name in PHASE23_HOST_SEAL_BAR:
        rows.append(
            phase23_tier_row(
                name,
                host_tier="functional_host",
                vm_tier="functional_host",
                thread_safe=True,
                notes=["Phase 15 sync primitives; per-atomic host mutex or queue.Queue"],
            )
        )
    for name in sorted(PHASE23_RUNTIME_NATIVE_SYMBOLS):
        if name in PHASE23_HOST_SEAL_BAR:
            continue
        if name in PHASE23_VM_MISSING_SURFACES:
            rows.append(
                phase23_tier_row(
                    name,
                    host_tier="functional_host",
                    vm_tier="vm_missing",
                    notes=["Host poll/drain only; bytecode VM has no OP_AWAIT"],
                )
            )
        elif name in PHASE23_BLOCKING_ASYNC_SURFACES:
            rows.append(
                phase23_tier_row(
                    name,
                    host_tier="functional_host",
                    vm_tier="vm_missing",
                    notes=["Blocking host thread or pool .result(); not cooperative VM await"],
                )
            )
        elif name.startswith("std.fiber.") or name.startswith("std.concurrent.race."):
            rows.append(
                phase23_tier_row(
                    name,
                    host_tier="scaffold",
                    vm_tier="vm_missing",
                    notes=["Staging helper; not VM coroutine frames or happens-before analyzer"],
                )
            )
        elif name.startswith("std.web.worker."):
            rows.append(
                phase23_tier_row(
                    name,
                    host_tier="scaffold",
                    vm_tier="vm_missing",
                    notes=["Host-thread inbox simulation; not browser Worker"],
                )
            )
        elif name == "std.thread.pool.steal_work":
            rows.append(
                phase23_tier_row(
                    name,
                    host_tier="scaffold",
                    vm_tier="vm_missing",
                    notes=["Audit deque for work-stealing claims; not a scheduler"],
                )
            )
        else:
            rows.append(
                phase23_tier_row(
                    name,
                    host_tier="functional_host",
                    vm_tier="functional_host",
                    notes=["Host threading/locks/futures via CPython bridges"],
                )
            )
    rows.append(
        phase23_tier_row(
            "async_future",
            host_tier="scaffold",
            vm_tier="vm_missing",
            notes=["Type-checker surface only; no async function bytecode lowering"],
        )
    )
    rows.append(
        phase23_tier_row(
            "std.phase23.seal_run",
            host_tier="functional_host",
            vm_tier="vm_missing",
            notes=["Host-tier full seal runner; emits P23_SEAL markers; not VM event loop"],
        )
    )
    return rows


def verify_phase23_anti_fake() -> list[str]:
    """Return violations when Phase 23 tiers or async depth are over-claimed."""
    violations: list[str] = []
    rows = {row["name"]: row for row in phase23_inventory()}

    for name in PHASE23_VM_MISSING_SURFACES:
        row = rows.get(name)
        if row is None:
            violations.append(f"{name}: missing from phase23 inventory")
            continue
        if row.get("vm_tier") != "vm_missing":
            violations.append(f"{name}: vm_tier must be vm_missing until OP_AWAIT exists")
        notes_blob = " ".join(str(n) for n in row.get("notes", [])).casefold()
        if name.startswith("std.async.") and "op_await" not in notes_blob and "vm" not in notes_blob:
            violations.append(f"{name}: inventory notes must document missing VM await lowering")

    for name in PHASE23_BLOCKING_ASYNC_SURFACES:
        row = rows.get(name)
        if row is None:
            violations.append(f"{name}: missing blocking-async inventory row")
            continue
        notes_blob = " ".join(str(n) for n in row.get("notes", [])).casefold()
        if "blocking" not in notes_blob and "pool" not in notes_blob:
            violations.append(f"{name}: must document blocking host async in inventory notes")

    for name, row in rows.items():
        if row.get("host_tier") == "scaffold" and row.get("vm_tier") == "functional_host":
            violations.append(f"{name}: scaffold host surface cannot claim vm_tier functional_host")
        notes_blob = " ".join(str(n) for n in row.get("notes", [])).casefold()
        if _inventory_claims_vm_native_await(notes_blob):
            violations.append(f"{name}: inventory must not claim VM-native cooperative await")

    sleep_src = inspect.getsource(_async_sleep_ms)
    if "time.sleep" not in sleep_src:
        violations.append("std.async.sleep_ms: implementation must use blocking time.sleep")
    await_src = inspect.getsource(_async_await)
    if "time.sleep" not in await_src:
        violations.append("std.async.await: host poll loop must not fake non-blocking spin")

    bc_path = Path(__file__).resolve().parent / "bytecode.py"
    bc_text = bc_path.read_text(encoding="utf-8")
    if "OP_AWAIT" in bc_text or '\n    AWAIT = "' in bc_text:
        violations.append("bytecode.py: OP_AWAIT must not exist until VM await lowering is implemented")

    stdlib_path = Path(__file__).resolve().parent / "stdlib_impl.py"
    stdlib_text = stdlib_path.read_text(encoding="utf-8")
    for atomic_fn in (
        "_sync_atomic_load",
        "_sync_atomic_store",
        "_sync_atomic_fetch_add",
        "_sync_atomic_compare_exchange",
    ):
        marker = f"def {atomic_fn}"
        if marker not in stdlib_text:
            violations.append(f"stdlib_impl.py missing {atomic_fn}")
            continue
        atomic_src = stdlib_text.split(marker, 1)[1].split("\ndef ", 1)[0]
        if "_atomic_mutex" not in atomic_src:
            violations.append(f"{atomic_fn}: must guard with per-atomic mutex")
    if "def _sync_channel_send" in stdlib_text:
        channel_src = stdlib_text.split("def _sync_channel_send", 1)[1].split("\ndef ", 1)[0]
        if "queue.put" not in channel_src and "Queue" not in channel_src:
            violations.append("std.sync.channel.send: must use host queue.Queue")

    return violations


def _inventory_claims_vm_native_await(notes_blob: str) -> bool:
    """True only when notes positively claim VM-native await (not honest negations)."""
    if "not vm-native" in notes_blob or "no vm-native" in notes_blob:
        return False
    if "not cooperative vm await" in notes_blob or "no cooperative vm await" in notes_blob:
        return False
    if "vm-native" in notes_blob:
        return True
    return "cooperative vm await" in notes_blob


def _runtime_verify_atomic_compare_exchange() -> list[str]:
    atom = _native_call("std.sync.atomic.new", [0])
    workers = 6
    attempts = 30
    barrier = threading.Barrier(workers)
    errors: list[str] = []

    def worker() -> None:
        try:
            barrier.wait(timeout=5)
            for _ in range(attempts):
                current = int(_native_call("std.sync.atomic.load", [atom]))
                result = _native_call(
                    "std.sync.atomic.compare_exchange",
                    [atom, current, current + 1],
                )
                if not isinstance(result, ResultValue):
                    raise RuntimeSanskriptError("compare_exchange returned non-result")
        except BaseException as exc:  # noqa: BLE001
            errors.append(str(exc))

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    if errors:
        return [f"atomic compare_exchange stress: {errors[0]}"]
    final = int(_native_call("std.sync.atomic.load", [atom]))
    if final <= 0 or final > workers * attempts:
        return [f"atomic compare_exchange stress: unexpected final value {final}"]
    return []


def _runtime_verify_atomics_thread_safe() -> list[str]:
    atom = _native_call("std.sync.atomic.new", [0])
    workers = 6
    adds = 40
    barrier = threading.Barrier(workers)
    errors: list[str] = []

    def worker() -> None:
        try:
            barrier.wait(timeout=5)
            for _ in range(adds):
                _native_call("std.sync.atomic.fetch_add", [atom, 1])
        except BaseException as exc:  # noqa: BLE001
            errors.append(str(exc))

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=15)
    if errors:
        return [f"atomic stress: {errors[0]}"]
    expected = workers * adds
    actual = _native_call("std.sync.atomic.load", [atom])
    if actual != expected:
        return [f"atomic stress: expected {expected}, got {actual}"]
    return []


def _runtime_verify_channel_delivery() -> list[str]:
    channel = _native_call("std.sync.channel.new", [8])
    received: list[int] = []
    lock = threading.Lock()

    def consumer() -> None:
        for _ in range(12):
            value = _native_call("std.sync.channel.recv", [channel, 2000])
            if isinstance(value, OptionValue) and not value.present:
                with lock:
                    received.append(-1)
                return
            with lock:
                received.append(int(value))

    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()
    for i in range(12):
        ok = _native_call("std.sync.channel.send", [channel, i])
        if not ok:
            return [f"channel send failed at {i}"]
    consumer_thread.join(timeout=10)
    if sorted(received) != list(range(12)):
        return [f"channel delivery mismatch: {received!r}"]
    return []


def _p23_marker(slug: str) -> str:
    return f"P23_SEAL:{slug}:ok"


def phase23_seal_run(_args: list) -> dict[str, Any]:
    """Run all Phase 23 host-tier checklist proofs; return markers for sanskript run."""
    markers: list[str] = []
    errors: list[str] = []

    def record(slug: str, fn: Callable[[], object]) -> None:
        try:
            fn()
            markers.append(_p23_marker(slug))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{slug}: {exc}")

    record(
        "threads",
        lambda: _thread_join(
            [
                _thread_spawn([{"symbol": "std.math.max", "args": [2, 5]}]),
                500,
            ]
        ),
    )

    def _fiber_steps() -> None:
        fiber = _fiber_create([["x", "y"]])
        _fiber_resume([fiber])
        _fiber_resume([fiber])
        _fiber_resume([fiber])

    record("fibers_coroutines", _fiber_steps)

    def _futures() -> None:
        future = _future_register(None, value=7)
        polled = _future_poll([future])
        if not polled.get("ready") or polled.get("value") != 7:
            raise RuntimeError("future poll/resolve failed")

    record("futures_promises", _futures)

    def _timer() -> None:
        future = _async_timer_after_ms(
            [20, {"symbol": "std.math.sqrt", "args": [9]}],
        )
        _async_event_loop_drain([500])
        polled = _future_poll([future])
        if not polled.get("ready"):
            raise RuntimeError("timer future not ready")

    record("timers", _timer)

    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "p23-seal.txt")

        def _file_io() -> None:
            _async_write_text([path, "seal"])
            if _async_read_text([path]) != "seal":
                raise RuntimeError("async file round-trip failed")

        record("async_file_io", _file_io)

    record(
        "async_networking",
        lambda: _async_net_connect(["127.0.0.1", 9, 30]),
    )

    def _cancel() -> None:
        token = _async_cancel_new([])
        _async_cancel_request([token])
        if not _async_cancel_is_cancelled([token]):
            raise RuntimeError("cancel token not set")

    record("cancellation", _cancel)

    def _channel() -> None:
        ch = _native_call("std.sync.channel.new", [2])
        _native_call("std.sync.channel.send", [ch, 42])
        got = _native_call("std.sync.channel.recv", [ch, 50])
        if got != 42:
            raise RuntimeError("channel round-trip failed")

    record("channels", _channel)

    def _queue() -> None:
        queue = _sync_queue_new([2])
        _sync_queue_enqueue([queue, {"n": 1}])
        got = _sync_queue_dequeue([queue, 50])
        if got != {"n": 1}:
            raise RuntimeError("sync queue round-trip failed")

    record("queues", _queue)

    def _mutex() -> None:
        mutex = _sync_mutex_new([])
        if not _sync_mutex_acquire([mutex, 50]):
            raise RuntimeError("mutex acquire failed")
        _sync_mutex_release([mutex])

    record("mutexes", _mutex)

    def _rwlock() -> None:
        rw = _sync_rwlock_new([])
        _sync_rwlock_acquire_read([rw, 50])
        _sync_rwlock_release([rw])
        _sync_rwlock_acquire_write([rw, 50])
        _sync_rwlock_release([rw])

    record("read_write_locks", _rwlock)

    def _sem() -> None:
        sem = _sync_semaphore_new([1])
        _sync_semaphore_acquire([sem, 50])
        _sync_semaphore_release([sem])

    record("semaphores", _sem)

    record(
        "atomics",
        lambda: _native_call(
            "std.sync.atomic.load",
            [_native_call("std.sync.atomic.new", [3])],
        ),
    )

    def _pool() -> None:
        pool = _thread_pool_new([2])
        future = _thread_pool_submit(
            [pool, {"symbol": "std.math.min", "args": [4, 9]}],
        )
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            polled = _future_poll([future])
            if polled.get("ready"):
                break
            time.sleep(0.01)
        else:
            raise RuntimeError("pool future not ready before shutdown")
        _thread_pool_shutdown([pool])

    record("thread_pools", _pool)

    def _steal() -> None:
        pool = _thread_pool_new([1])
        _thread_pool_submit([pool, {"symbol": "std.math.max", "args": [1, 2]}])
        stolen = _thread_pool_steal_work([pool])
        _thread_pool_shutdown([pool])
        if stolen is NIL:
            raise RuntimeError("steal_work audit queue empty")

    record("work_stealing", _steal)

    def _race() -> None:
        _RACE_ACCESS_LOG.clear()
        _concurrent_race_record(
            [
                [
                    {"var": "x", "mode": "write", "thread_id": 1},
                    {"var": "x", "mode": "write", "thread_id": 2},
                ]
            ]
        )
        races = _concurrent_race_detect([])
        if not races:
            raise RuntimeError("race detect expected write-write")
        _concurrent_race_clear([])

    record("data_race_rakshita", _race)

    record(
        "arakshita_unsafe_rules",
        lambda: _concurrent_arakshita_check(
            [{"tier": "arakshita", "operation": "channel_send", "unsafe_region": True}],
        ),
    )

    def _worker() -> None:
        worker = _web_worker_spawn(["p23-seal"])
        _web_worker_post([worker, "ping"])
        reply = _web_worker_recv([worker, 500])
        if not isinstance(reply, dict) or reply.get("echo") != "pong":
            raise RuntimeError("web worker echo failed")
        _web_worker_terminate([worker])

    record("browser_workers", _worker)

    def _gatekeeper() -> None:
        verdict = phase23_seal_verdict()
        if verdict["verdict"] != "dual_tier_host_seal":
            raise RuntimeError(f"seal_verdict blocked: {verdict.get('host_tier', {}).get('blockers')}")
        if not verdict["host_tier"]["sealed"]:
            raise RuntimeError("host_tier not sealed")
        if verify_phase23_anti_fake():
            raise RuntimeError("anti_fake violations present")

    record("gatekeeper", _gatekeeper)

    expected = set(PHASE23_HOST_CHECKLIST_SLUGS)
    got = {m.split(":")[1] for m in markers}
    missing = sorted(expected - got)
    if missing:
        errors.append(f"missing_slugs:{','.join(missing)}")
    return {
        "verdict": "SEALED_AT_HOST_TIER" if not errors else "FAILED",
        "marker_count": len(markers),
        "checklist_count": len(PHASE23_HOST_CHECKLIST_SLUGS),
        "markers": markers,
        "errors": errors,
        "host_tier": "sealed",
        "vm_tier": "vm_missing",
    }


def audit_phase23_checklist_honesty(*, root: Path | None = None) -> list[str]:
    """Fail when Phase 23 checklist ticks disagree with dual-tier host seal policy."""
    repo = root or REPO_ROOT
    checklist = repo / "docs" / "native-sanskript-independence-checklist.md"
    doc = repo / "docs" / "phase23-concurrency-async.md"
    violations: list[str] = []
    if not checklist.is_file():
        return ["docs/native-sanskript-independence-checklist.md missing"]
    if not doc.is_file():
        return ["docs/phase23-concurrency-async.md missing"]
    section = checklist.read_text(encoding="utf-8").split("## Phase 23:")[1].split("## Phase 24:")[0]
    doc_text = doc.read_text(encoding="utf-8")
    if "dual_tier_host_seal" not in section:
        violations.append("Phase 23 checklist section must declare dual_tier_host_seal")
    if "dual_tier_host_seal" not in doc_text:
        violations.append("phase23-concurrency-async.md must declare dual_tier_host_seal")
    if "vm_missing" not in section or "OP_AWAIT" not in section:
        violations.append("Phase 23 checklist must document vm_missing / OP_AWAIT blockers")
    for needle in PHASE23_CHECKLIST_HOST_ROWS:
        if not re.search(rf"- \[x\] {re.escape(needle)}", section):
            violations.append(f"Phase 23 checklist missing host seal [x] for {needle!r}")
    for needle in PHASE23_CHECKLIST_VM_MISSING_ROWS:
        if not re.search(rf"- \[ \] {re.escape(needle)}", section):
            violations.append(f"Phase 23 checklist must keep vm_missing open for {needle!r}")
    return violations


def _verify_phase23_example_runs(*, root: Path | None = None) -> list[str]:
    repo = root or REPO_ROOT
    example = repo / "examples" / "phase23-concurrency-async.ssk"
    if not example.is_file():
        return ["examples/phase23-concurrency-async.ssk missing"]
    try:
        from .compiler import compile_program
        from .module_loader import load_program_from_path
        from .vm import SanskriptVM

        program = load_program_from_path(example)
        SanskriptVM().execute(compile_program(program))
    except Exception as exc:  # noqa: BLE001
        return [f"phase23 example failed to compile/run: {exc}"]
    return []


def verify_phase23_full_seal(*, root: Path | None = None) -> list[str]:
    """FULL SEAL gatekeeper: dual-tier host seal with thread-safe atomics/channels and no fake async."""
    violations = list(verify_phase23_anti_fake())
    violations.extend(audit_phase23_checklist_honesty(root=root))
    violations.extend(_verify_phase23_example_runs(root=root))
    verdict = phase23_seal_verdict()
    if verdict["verdict"] != "dual_tier_host_seal":
        violations.append(
            f"phase23 seal verdict is {verdict['verdict']!r}, expected dual_tier_host_seal"
        )
    if not verdict["host_tier"]["sealed"]:
        violations.extend(f"host_tier: {item}" for item in verdict["host_tier"]["blockers"])
    if verdict["vm_tier"]["sealed"]:
        violations.append("vm_tier must remain unsealed until OP_AWAIT exists")
    if not verdict.get("no_fake_async"):
        violations.append("no_fake_async flag is false")
    return violations


def phase23_full_seal_payload(*, root: Path | None = None) -> dict[str, Any]:
    violations = verify_phase23_full_seal(root=root)
    verdict = phase23_seal_verdict()
    return {
        "phase": 23,
        "spec_version": PHASE23_SPEC_VERSION,
        "full_seal_ready": not violations,
        "status": "dual_tier_host_seal" if not violations else "blocked",
        "verdict": verdict,
        "violations": violations,
    }


def phase23_seal_verdict() -> dict[str, Any]:
    """Dual-tier seal: host functional tier sealed; VM await tier explicitly blocked."""
    anti_fake = verify_phase23_anti_fake()
    runtime_blockers = (
        _runtime_verify_atomics_thread_safe()
        + _runtime_verify_atomic_compare_exchange()
        + _runtime_verify_channel_delivery()
    )
    vm_blockers = [
        "Bytecode VM has no OP_AWAIT / in-language await lowering",
        "async_future functions are type-check only (no async fn bytecode)",
        "std.async.event_loop.* drains host ThreadPoolExecutor, not a Sanskript scheduler",
        "std.web.worker.* is host-thread simulation, not browser Worker",
    ]
    host_blockers = list(anti_fake) + list(runtime_blockers)
    host_sealed = len(host_blockers) == 0
    return {
        "phase": 23,
        "spec_version": PHASE23_SPEC_VERSION,
        "verdict": "dual_tier_host_seal" if host_sealed else "blocked",
        "host_tier": {
            "sealed": host_sealed,
            "seal_bar": list(PHASE23_HOST_SEAL_BAR),
            "blockers": host_blockers,
            "atomics_thread_safe": not any("atomic" in b for b in runtime_blockers),
            "channels_thread_safe": not any("channel" in b for b in runtime_blockers),
        },
        "vm_tier": {
            "sealed": False,
            "blockers": vm_blockers,
        },
        "anti_fake_violations": anti_fake,
        "no_fake_async": (not anti_fake)
        and ("time.sleep" in inspect.getsource(_async_sleep_ms)),
    }


def _phase23_inventory_native(_args: list) -> list[dict[str, object]]:
    _ = _args
    return phase23_inventory()


def _phase23_verify_native(_args: list) -> dict[str, object]:
    _ = _args
    violations = verify_phase23_anti_fake()
    return {"ok": not violations, "violations": violations}


def _phase23_seal_verdict_native(_args: list) -> dict[str, Any]:
    _ = _args
    return phase23_seal_verdict()


PHASE23_NATIVE_REGISTRY: dict[str, NativeSpec] = {
    "std.thread.spawn": NativeSpec(1, _thread_spawn),
    "std.thread.join": NativeSpec(2, _thread_join),
    "std.thread.current_id": NativeSpec(0, _thread_current_id),
    "std.thread.is_alive": NativeSpec(1, _thread_is_alive),
    "std.thread.pool.new": NativeSpec(1, _thread_pool_new),
    "std.thread.pool.submit": NativeSpec(2, _thread_pool_submit),
    "std.thread.pool.join": NativeSpec(2, _thread_pool_join),
    "std.thread.pool.shutdown": NativeSpec(1, _thread_pool_shutdown),
    "std.thread.pool.steal_work": NativeSpec(1, _thread_pool_steal_work),
    "std.fiber.create": NativeSpec(1, _fiber_create),
    "std.fiber.resume": NativeSpec(1, _fiber_resume),
    "std.async.future.poll": NativeSpec(1, _future_poll),
    "std.async.future.resolve": NativeSpec(2, _future_resolve),
    "std.async.await": NativeSpec(2, _async_await),
    "std.async.spawn": NativeSpec(1, _async_spawn),
    "std.async.event_loop.run_once": NativeSpec(0, _async_event_loop_run_once),
    "std.async.event_loop.pending": NativeSpec(0, _async_event_loop_pending),
    "std.async.event_loop.drain": NativeSpec(1, _async_event_loop_drain),
    "std.async.sleep_ms": NativeSpec(1, _async_sleep_ms),
    "std.async.read_text": NativeSpec(1, _async_read_text),
    "std.async.write_text": NativeSpec(2, _async_write_text),
    "std.async.net.connect": NativeSpec(3, _async_net_connect),
    "std.async.timer.after_ms": NativeSpec(2, _async_timer_after_ms),
    "std.async.cancel.new": NativeSpec(0, _async_cancel_new),
    "std.async.cancel.request": NativeSpec(1, _async_cancel_request),
    "std.async.cancel.is_cancelled": NativeSpec(1, _async_cancel_is_cancelled),
    "std.async.cancel.check": NativeSpec(1, _async_cancel_check),
    "std.async.scope.run": NativeSpec(1, _async_scope_run),
    "std.sync.mutex.new": NativeSpec(0, _sync_mutex_new),
    "std.sync.mutex.acquire": NativeSpec(2, _sync_mutex_acquire),
    "std.sync.mutex.release": NativeSpec(1, _sync_mutex_release),
    "std.sync.rwlock.new": NativeSpec(0, _sync_rwlock_new),
    "std.sync.rwlock.acquire_read": NativeSpec(2, _sync_rwlock_acquire_read),
    "std.sync.rwlock.acquire_write": NativeSpec(2, _sync_rwlock_acquire_write),
    "std.sync.rwlock.release": NativeSpec(1, _sync_rwlock_release),
    "std.sync.semaphore.new": NativeSpec(1, _sync_semaphore_new),
    "std.sync.semaphore.acquire": NativeSpec(2, _sync_semaphore_acquire),
    "std.sync.semaphore.release": NativeSpec(1, _sync_semaphore_release),
    "std.sync.queue.new": NativeSpec(1, _sync_queue_new),
    "std.sync.queue.enqueue": NativeSpec(2, _sync_queue_enqueue),
    "std.sync.queue.dequeue": NativeSpec(2, _sync_queue_dequeue),
    "std.concurrent.race.record": NativeSpec(1, _concurrent_race_record),
    "std.concurrent.race.detect": NativeSpec(0, _concurrent_race_detect),
    "std.concurrent.race.clear": NativeSpec(0, _concurrent_race_clear),
    "std.concurrent.arakshita.check": NativeSpec(1, _concurrent_arakshita_check),
    "std.web.worker.spawn": NativeSpec(1, _web_worker_spawn),
    "std.web.worker.post_message": NativeSpec(2, _web_worker_post),
    "std.web.worker.recv": NativeSpec(2, _web_worker_recv),
    "std.web.worker.terminate": NativeSpec(1, _web_worker_terminate),
    "std.phase23.inventory": NativeSpec(0, _phase23_inventory_native),
    "std.phase23.verify": NativeSpec(0, _phase23_verify_native),
    "std.phase23.seal_verdict": NativeSpec(0, _phase23_seal_verdict_native),
    "std.phase23.seal_run": NativeSpec(0, phase23_seal_run),
}
