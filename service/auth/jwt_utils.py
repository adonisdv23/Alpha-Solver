import base64
import json
import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional
import tempfile

import yaml

ALLOWED_ALGS = {"RS256"}
LEWAY_SECONDS = 60


class JWTError(Exception):
    """Exception raised for JWT validation issues."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class AuthKeyStore:
    """Key store backed by a YAML file mapping kid -> PEM public key."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._keys: Dict[str, str] = {}
        # track file modification time with nanosecond precision so that
        # rapid rotations inside tests are detected reliably
        self._mtime_ns: int = 0
        self.reload(force=True)

    def reload(self, force: bool = False) -> None:
        try:
            mtime = self.path.stat().st_mtime_ns
        except FileNotFoundError:
            self._keys = {}
            self._mtime_ns = 0
            return
        if force or mtime != self._mtime_ns:
            with self.path.open() as f:
                data = yaml.safe_load(f) or {}
            keys: Dict[str, str] = {}
            for kid, value in data.items():
                if isinstance(value, dict):
                    pem = value.get("public_key") or value.get("key") or ""
                else:
                    pem = value or ""
                keys[kid] = pem
            self._keys = keys
            self._mtime_ns = mtime

    def get_key(self, kid: str) -> Optional[str]:
        self.reload()
        return self._keys.get(kid)


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


logger = logging.getLogger("service.auth.jwt")


def verify_jwt(
    token: str,
    key_store: AuthKeyStore,
    audience: str | None = None,
    issuer: str | None = None,
    leeway: int = LEWAY_SECONDS,
) -> Dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise JWTError("invalid_header", "malformed token")
    header_b64, payload_b64, sig_b64 = parts
    try:
        header = json.loads(_b64url_decode(header_b64))
    except Exception:
        raise JWTError("invalid_header", "malformed token header")

    alg = header.get("alg")
    if alg not in ALLOWED_ALGS:
        raise JWTError("invalid_alg", "unsupported signing algorithm")

    kid = header.get("kid")
    if not kid:
        raise JWTError("missing_kid", "kid header missing")

    key = key_store.get_key(kid)
    if not key:
        raise JWTError("unknown_kid", "unknown key id")

    try:
        signature = _b64url_decode(sig_b64)
    except Exception:
        raise JWTError("invalid_token", "invalid signature")

    signing_input = f"{header_b64}.{payload_b64}".encode()
    # verify using openssl
    with tempfile.NamedTemporaryFile("w", delete=False) as kf:
        kf.write(key)
        kf.flush()
        key_path = kf.name
    try:
        with tempfile.NamedTemporaryFile() as df, tempfile.NamedTemporaryFile() as sf:
            df.write(signing_input)
            df.flush()
            sf.write(signature)
            sf.flush()
            proc = subprocess.run(
                [
                    "openssl",
                    "dgst",
                    "-sha256",
                    "-verify",
                    key_path,
                    "-signature",
                    sf.name,
                    df.name,
                ],
                capture_output=True,
            )
            if proc.returncode != 0:
                raise JWTError("invalid_token", "invalid signature")
    finally:
        try:
            os.unlink(key_path)
        except OSError:
            pass

    try:
        payload = json.loads(_b64url_decode(payload_b64))
    except Exception:
        raise JWTError("invalid_token", "malformed payload")

    now = int(time.time())
    exp = payload.get("exp")
    if exp is not None and now > int(exp) + leeway:
        raise JWTError("token_expired", "token expired")
    nbf = payload.get("nbf")
    if nbf is not None and now + leeway < int(nbf):
        raise JWTError("token_not_yet_valid", "token not yet valid")
    if audience and payload.get("aud") != audience:
        raise JWTError("invalid_audience", "invalid audience")
    if issuer and payload.get("iss") != issuer:
        raise JWTError("invalid_issuer", "invalid issuer")
    return payload


__all__ = ["AuthKeyStore", "JWTError", "verify_jwt", "ALLOWED_ALGS"]
