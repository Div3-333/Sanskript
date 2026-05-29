# Phase 23: Concurrency And Async

**SEALED at host tier** (`dual_tier_host_seal`). All host/scaffold checklist rows are proven via `python -m sanskript.cli run examples/phase23-full-seal.ssk` (`std.phase23.seal_run` emits `P23_SEAL:<slug>:ok` markers). Host-Python threading bridges implement the seal bar (atomics with per-handle mutex, `queue.Queue` channels, threads, sync primitives) with runtime stress proof in `phase23_seal_verdict()`. The bytecode VM still has **no** `OP_AWAIT` / `await` lowering, no in-language event loop, and no browser `Worker` integration — **`vm_missing`** rows (async functions, await, event loop, structured concurrency) stay open. `std.async.sleep_ms` and pool-based async I/O **block the calling host thread**; they are not cooperative VM await.

## Host-tier full seal

| Artifact | Command | Test |
| --- | --- | --- |
| All 18 host `[x]` rows | `python -m sanskript.cli run examples/phase23-full-seal.ssk` | `tests/test_phase23_concurrency_async.py::Phase23FullSealTests::test_phase23_full_seal_example_executes` |
| Seal matrix native | (inside full-seal JSON) | `...::test_phase23_seal_run_native_passes` |

## Tier labels

| Tier | Meaning |
| --- | --- |
| **functional_host** | Callable from Sanskript via native registry; semantics run on the CPython host (threads, locks, pools). |
| **scaffold** | Staged API or audit hook; not a production scheduler/DOM worker runtime. |
| **vm_missing** | Type checker or docs may mention the feature; bytecode VM cannot suspend/resume or schedule it. |

## Capability map (honest)

| Area | Tier | Notes |
| --- | --- | --- |
| Threads, pools, work-steal audit queue | functional_host | `std.thread.*` on `threading` / `ThreadPoolExecutor`. |
| Fibers (`std.fiber.*`) | scaffold | Cooperative step deque; not VM coroutine frames. |
| Async function typing | vm_missing | `async_future` in type checker only. |
| `std.async.await`, event loop, structured scope | vm_missing | Host poll/drain over `ThreadPoolExecutor`; blocks calling thread. |
| Futures, timers, cancellation | functional_host | Host futures / `threading.Timer`; not VM scheduled tasks. |
| `std.async.sleep_ms`, async file/net I/O | functional_host | **Blocking** host sleep or pool `.result()` — see blocking-async test. |
| Mutex / rwlock / semaphore / queue (Phase 23) | functional_host | Host locks; Phase 15 channels/atomics unchanged. |
| Atomics / channels (Phase 15) | functional_host | Per-atomic mutex in `stdlib_impl.py`; contention-safe under host threads. |
| `std.concurrent.race.*` | scaffold | Trace log for `rakṣita` audits; not a happens-before analyzer. |
| `std.concurrent.arakshita.check` | functional_host | Policy gate for unsafe regions. |
| `std.web.worker.*` | scaffold | Host-thread inbox simulation; **not** browser `Worker`. |

## Enforcement surfaces

- Runtime primitives: `src/sanskript/phase23_concurrency.py` (registered through `stdlib_impl.NATIVE_REGISTRY`).
- Static async/tier guards: `src/sanskript/type_checker.py` (`_check_phase23_concurrency_rules`).
- Existing sync/atomic/channel baseline: `std.sync.*`, `std.thread.marker.*` from Phase 15.
- Tests: `tests/test_phase23_concurrency_async.py` (positive, stress, blocking-async honesty, atomic contention).

## Threads and pools (functional_host)

- `std.thread.spawn` / `std.thread.join` / `std.thread.current_id` / `std.thread.is_alive`
- `std.thread.pool.new` / `submit` / `join` / `shutdown` / `steal_work` (work-stealing audit queue)

Thread spawn descriptors use `{symbol, args}` maps and execute allowlisted native calls on host threads.

## Fibers / coroutines (scaffold)

- `std.fiber.create` builds a cooperative step queue.
- `std.fiber.resume` yields `{done, value}` records until exhaustion.

Coroutine/async function typing (`async_future`, `coroutine`, `generator`) remains in the type checker; runnable host fibers are staging only.

## Async / futures / event loop (vm_missing + functional_host)

| Symbol | Tier |
| --- | --- |
| `std.async.future.poll`, `resolve` | functional_host |
| `std.async.await` | vm_missing |
| `std.async.spawn`, `event_loop.*`, `scope.run` | vm_missing |
| `std.async.timer.after_ms`, `cancel.*` | functional_host |
| `std.async.sleep_ms`, `read_text`, `write_text`, `net.connect` | functional_host (blocking host thread or blocking pool `.result()`) |

`std.async.sleep_ms` uses `time.sleep` on the **calling host thread** — not cooperative VM await. Tests document this explicitly.

## Sync primitives (functional_host)

- Mutexes: `std.sync.mutex.new` / `acquire` / `release`
- RW locks: `std.sync.rwlock.new` / `acquire_read` / `acquire_write` / `release`
- Semaphores: `std.sync.semaphore.new` / `acquire` / `release`
- Queues: `std.sync.queue.new` / `enqueue` / `dequeue`
- Phase 15 atomics/channels/locks: `std.sync.atomic.*`, `std.sync.channel.*`, `std.sync.lock.*`

Send-safe payload rules apply to queues/channels/worker messages.

## Data race checking (`rakṣita`, scaffold)

- `std.concurrent.race.record` ingests access events `{var, mode, thread_id}`.
- `std.concurrent.race.detect` reports write-write and read-write races across threads.
- `std.concurrent.race.clear` resets the trace log.

## Unsafe concurrent rules (`arakṣita`, functional_host)

- `std.concurrent.arakshita.check` validates policy maps and rejects channel/shared-mut operations outside explicit unsafe regions.
- Compile-time guard rejects `channel` aliases in `arakṣita` and blocks `async_future` functions from taking `raw_ptr_mut` / `borrow_mut` parameters.

## Browser workers (scaffold)

- `std.web.worker.spawn` / `post_message` / `recv` / `terminate`
- Host-thread worker simulation with send-safe message envelopes — **not** browser `Worker` APIs.

## Migration notes

- Programs using only `std.async.sleep_ms` from Phase 14 can adopt event-loop APIs without source changes; behavior remains host-blocking until VM await exists.
- Cross-thread payloads should pass `std.thread.marker.send` before queue/channel enqueue.
- `arakṣita` code must keep channel operations inside unsafe regions or migrate to explicit memory + atomic fences.

## Gatekeeper

- `std.phase23.seal_run` — host-tier full seal runner (`P23_SEAL:<slug>:ok` for all 19 host/scaffold rows).
- `std.phase23.inventory` — dual-tier rows (`host_tier`, `vm_tier`, `thread_safe` where applicable).
- `std.phase23.verify` — anti-fake static checks (blocking async, no `OP_AWAIT` over-claim).
- `std.phase23.seal_verdict` — host runtime stress for atomics/channels + explicit VM blockers.
- `python -m sanskript.cli phase23-seal` — **FULL SEAL** gatekeeper (`verify_phase23_full_seal`: checklist honesty, example compile/run, runtime atomics/CAS/channels stress, `no_fake_async`).
- Tests: `Phase23SealGatekeeperTests` in `tests/test_phase23_concurrency_async.py`.

## Validation

```bash
python -m pytest tests/test_phase23_concurrency_async.py -q
python -m sanskript.cli run examples/phase23-concurrency-async.ssk
```
