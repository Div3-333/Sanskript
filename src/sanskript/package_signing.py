from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass
from pathlib import Path

from .errors import CompileError

DEFAULT_SIGNING_SECRET = "sanskript-dev-signing-key"


@dataclass(frozen=True)
class SignatureRecord:
    algorithm: str
    digest: str
    signature: str


def package_digest(root: Path, *, extra: bytes = b"") -> str:
    hasher = hashlib.sha256()
    hasher.update(extra)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name in {"ssk.lock", "ssk.toml", "saṃskaraṇa.sskm", "samskarana.sskm"}:
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        hasher.update(rel.encode("utf-8"))
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def sign_digest(digest: str, *, secret: str | None = None) -> SignatureRecord:
    key = (secret or os.environ.get("SANSKRIPT_SIGNING_KEY") or DEFAULT_SIGNING_SECRET).encode("utf-8")
    signature = hmac.new(key, digest.encode("utf-8"), hashlib.sha256).hexdigest()
    return SignatureRecord(algorithm="hmac-sha256", digest=digest, signature=signature)


def verify_signature(
    digest: str,
    signature: str,
    *,
    secret: str | None = None,
    on_failure: callable | None = None,
) -> bool:
    expected = sign_digest(digest, secret=secret).signature
    ok = hmac.compare_digest(expected, signature)
    if not ok and on_failure is not None:
        on_failure(digest, signature, expected)
    return ok


def verify_package_signature(root: Path, signature: str | None) -> None:
    if not signature:
        return
    digest = package_digest(root)
    if not verify_signature(digest, signature):
        raise CompileError(
            "Package signature verification failed",
            hint="Set SANSKRIPT_SIGNING_KEY or update the manifest signature after signing.",
            code="SANSKRIPT_PACKAGE_SIGNATURE",
        )


def sign_package(root: Path, *, secret: str | None = None) -> str:
    return sign_digest(package_digest(root), secret=secret).signature


__all__ = [
    "SignatureRecord",
    "package_digest",
    "sign_digest",
    "sign_package",
    "verify_package_signature",
    "verify_signature",
]
