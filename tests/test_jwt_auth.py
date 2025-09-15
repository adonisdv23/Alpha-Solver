import base64
import hmac
import json
import logging
import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import hashlib
import yaml
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from service.auth.jwt_utils import AuthKeyStore
from service.middleware.jwt_middleware import JWTAuthMiddleware

PRIV_KEY1 = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDH7neaSuButOWX
o+dPWsP2VxNEQlZXywjw7KJGaMDsJP/9d1aktm3y3q8+Z1ZyMSE3AcS580ZitfS3
mSV1CXijRSWNjn5nyX1T0xRxEBdf1vOqneillv7H8QTBSZ6SJvJoVcGpq7eLUo9E
JH+DB7lI3iXdKAW4lf9lX2NwsZfk82oxULDU1fEhIcvZk7hGr7TY77DKW5W+JlVI
+TNlQAsJKUR0kQQ/z0zuDxAYYe0IVdSnFFwiGzj34VHp20g3Etv97xkm0LGQHPXx
js7vEev3k1IXEncGB0Bcj8SHgmgH+izG7TkSwus3ql4RZou1KGm/SnIOEmjY+bt1
hOHBXyMLAgMBAAECggEAALq2MObrUaEmzYWVXTexCS/NOfA4adyZbXNhtGCmZ2y3
w7zVcmrJ58MdabtvlfvSYW0+LwN/WXzxCgoFk8DYqZM/5n9N3WRX77pvVTnbCvAv
Srn7Lbollg/U73M4tVraQKvVBCDMBPjyHJo23wJZkxeHbd34xjHQqd4tm9jdTNFi
qMCcsK50iUk3WINkOcFdGDzrjicJNo8Gtt62Hw+3iY34ctZQxJjkU4x1F6xU13NS
17AWUoTvkd+3FTRsbp5l/Ju58l3xCym28eYIiE/rtIQ7Bd9qMhScCZxOKhJfQ9HH
vW+DwNQYBXvCqeNCsHpLYdkzec/+wKIhZkDWHUiHYQKBgQD4itvOB0aFOn4x4N6b
s2/P+ZqecPWq4VQYKIEJncjGtAOX7u5sNntfZwQt9xZrmcxBMWbBtSFmtTesQ+/b
kAWNB7I4uMYxywHUpeSj/pLWqT8aCEXT+JebPGGqXlPhkOQncK8Fi92OAwY2uF1n
nYMeDOW72+XcA1rbBcvkR73FIQKBgQDN7jYRKy4plNTZTi3q9DLlhPk3zKSe2UOw
b491gBXVPZgUu522kly++v0FEwPqx2F14ZAQVNCIOIgO3161bVRAbGnY9D+S2a2m
P3zCIULUagfKs6XFDuEam3nsAMLsGSLM47LL95SeDOWNuF3aJ4+gdqrsTOFcmYRv
8hMcBZe2qwKBgQDtTzBmfN3hsaLynwIN6nt1OZ9fbv2yZil0U6A5fVVKHHFd7T3r
Ru3vfp4oAUd//75d9PxnMjotJhR9P/TSUKZsLRAHRq2+t1YNI0S3LQgpPDpK8eEy
bqbbCwE5uY0fz8d4vQfwJMarpMmXD9vnZibeV3Q3NdQ4iV+DxvoSAkn44QKBgAzX
mSmS7ssLDAcNOBHZ7r6ff0c6jN2XIQCExIaIWVQ2BiDs3lX/ZKdIUbUaTXk7u9k1
Gt3Z3DNSizGaPnbD/agS2rr76GcJCio+9VHJ7zf98MR0VZcnaWRWY9ES7xT4MFJk
tMbBhtQga8RdxgSPyQYxwFECLl+u9zJf/08VDjQHAoGAS3ukwcQwh362Zae92a1D
UdrQD3M5SThPngvTN1AQeLTxk4cmdrSgDoC3I3XWgtB0MKI4R1ia7IrrxdSlUFft
CtRlmOZAnvS2dloUVnG4fdZHZaalszLTSyLfq4tQyCyEs7GE2h6Zj/mZO2CEc72F
KsSOCM0/LOu/piGzbzrDs2c=
-----END PRIVATE KEY-----"""

PRIV_KEY2 = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCeEZXMA52KfT14
Qh1gKkNNHZIODrZyvxuQROveOi+QYIoheYSjKE2pWzZbcrVPxKdtcGDbpIuY/z1K
OhlirxxiTwM5KdpWIeXbgqxuzXyaUlZL6O0iDKev0R6paRZRctRlEePZQOCEjGl0
x3P7V302CsK44LbYdWBXjYpZljMcsrfWg4CiJ/Y7VNdwqg2zXyvgR6/QuMinioFX
pozEWCmytkLIcFWvZBDBJKpE/GnUTubau25a4GO0yU5iVXrM3jJUTH72h0lLK9yV
thGc+4nUKVhs0AAqBX1x3ffEYkrTIZZ2+XMlx/98dlLRFz0LVETePvkS8Mububqy
4qWCAhdRAgMBAAECggEAISNnp69EWnHaLrmRpgUGOgcOhTLxbgoBsdO5LUw+h4Kt
wsnSlFARRAWS1kYsm84LGcb7D2EmQQuVolee1dEHXtbYwqWzF+agZU42bz5WNpY3
cE+jU0Wa7CGnz3VwD+BGhe/juDrBNximzSw5dQKJBgjofNDjlGq7KW/Lhu+VxJig
YOLnQV8liBX9z7xlqcJ+ZMomBuMk/lUypQlMwDYYIjffJTTezb3DbpZX7ObA9LGz
aPtAjSuGhkfx2NWvxmWILWBG3TJHOOB51rVH1uEX0VTGpz7qeLt37R3irQPpnHTT
JjTkJaCdrHA1Nt8RC5TD2mMl9E6+dyyF1rFOLE0vSQKBgQDfd7PDMZ0lifOhAGId
GF+DJRNa2X2DmiPKlra49Qjv9vm9M+HA8L5qa5lYXdMOahNZbD/WbqmXgpf3hmkb
/Csx6XjShGgJ+htBio+kWd/ffPzWwU992jqWih6uQPgnjyRVHQkptPNgzJwqwHPC
LDJnADiN4ZxgYfL40xlWImDG1QKBgQC1FJC9ve8M0Lp0WZBwwZojNyfex5qYagdY
JKr3SSPvnfr4inLWUcRvwzpjy3rSFfSPoHYRfcdAR5LxWpOVu5Lb/h3tuZWCPcuW
URpvm1o4VIkehGQqQu/1eWZ4Z1V7O0xnXsN/ToOZvS+VUI1FjV4UGnf1UMlxpWW8
9eQbIFREjQKBgH0h8F1K+O4+U1hCeK5GKaWsKyxiQTBiLcyRnHvxajHFII9b7/w0
UswQuGuNDlQx/efC//Q5P2oBzMrkTxNGn4FxdSCc2A1OKdkHl+u2D/B7crFmyfZ1
Lv2BFjEJXGv6caPfgHQESYxYxtIBtlByoz6eFw0L2p71+jJvMu7SjVKJAoGAWdnN
hEjlf/9mNWtnr3txRz4MC5ARlsUtxb/UEYX6TeCe8oqINu41wZsmsvP5ipsYUdg2
HbHCl5OsRxRBnQ+I7J4oLZhjpk+RYJH3wx9b4g2YSEs7BHlYZf6KKP5lPROMctJj
wRytUjC8lqN0pelioCkOEuy2OCzw0ZVVTVx6U9UCgYA2bMmVqMQzvLSFFI16hZqF
WAQvx1jqUU9mCvhBd6TS3jAxPxCy9jX1aCVe1TSqt+/8FFbSnEAA7PblVH72ySXu
BrG1lOeqJ29hPDRZRPpI4xLGW8GGI5joqk534DPc4eCx0aHspyxYLxVqpvM9r7mj
9AeUoZB0ZYul6QtsTFUO1w==
-----END PRIVATE KEY-----"""

PUB_KEY2 = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnhGVzAOdin09eEIdYCpD
TR2SDg62cr8bkETr3jovkGCKIXmEoyhNqVs2W3K1T8SnbXBg26SLmP89SjoZYq8c
Yk8DOSnaViHl24Ksbs18mlJWS+jtIgynr9EeqWkWUXLUZRHj2UDghIxpdMdz+1d9
NgrCuOC22HVgV42KWZYzHLK31oOAoif2O1TXcKoNs18r4Eev0LjIp4qBV6aMxFgp
srZCyHBVr2QQwSSqRPxp1E7m2rtuWuBjtMlOYlV6zN4yVEx+9odJSyvclbYRnPuJ
1ClYbNAAKgV9cd33xGJK0yGWdvlzJcf/fHZS0Rc9C1RE3j75EvDLm7m6suKlggIX
UQIDAQAB
-----END PUBLIC KEY-----"""


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def sign(payload, key_pem, kid):
    header = {"alg": "RS256", "typ": "JWT", "kid": kid}
    header_b64 = b64url(json.dumps(header).encode())
    payload_b64 = b64url(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    with tempfile.NamedTemporaryFile("w", delete=False) as kf:
        kf.write(key_pem)
        kf.flush()
        key_path = kf.name
    try:
        with tempfile.NamedTemporaryFile() as df, tempfile.NamedTemporaryFile() as sf:
            df.write(signing_input)
            df.flush()
            subprocess.run(
                ["openssl", "dgst", "-sha256", "-sign", key_path, "-out", sf.name, df.name],
                check=True,
            )
            sf.seek(0)
            sig = sf.read()
    finally:
        os.unlink(key_path)
    sig_b64 = b64url(sig)
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def sign_hs(payload, secret):
    header = {"alg": "HS256", "typ": "JWT", "kid": "kid1"}
    header_b64 = b64url(json.dumps(header).encode())
    payload_b64 = b64url(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return f"{header_b64}.{payload_b64}.{b64url(sig)}"


def build_app(tmp_path: Path):
    original = Path("service/config/auth_keys.yaml").read_text()
    auth_path = tmp_path / "auth_keys.yaml"
    auth_path.write_text(original)
    store = AuthKeyStore(auth_path)
    app = FastAPI()
    app.add_middleware(JWTAuthMiddleware, key_store=store)

    @app.get("/protected")
    async def protected(request: Request):
        return request.state.principal

    return app, store, auth_path


def test_valid_jwt(tmp_path):
    app, _store, _path = build_app(tmp_path)
    client = TestClient(app)
    now = datetime.utcnow()
    token = sign({"sub": "u1", "tenant": "t1", "roles": ["r"], "exp": int((now + timedelta(minutes=5)).timestamp())}, PRIV_KEY1, "kid1")
    r = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["sub"] == "u1"
    assert r.json()["tenant_id"] == "t1"
    assert r.json()["roles"] == ["r"]


def test_expired_and_nbf(tmp_path):
    app, _store, _path = build_app(tmp_path)
    client = TestClient(app)
    now = datetime.utcnow()
    expired = sign({"sub": "u", "tenant": "t", "exp": int((now - timedelta(minutes=2)).timestamp())}, PRIV_KEY1, "kid1")
    r = client.get("/protected", headers={"Authorization": f"Bearer {expired}"})
    assert r.status_code == 401
    assert r.json()["code"] == "token_expired"
    future = sign({"sub": "u", "tenant": "t", "nbf": int((now + timedelta(minutes=5)).timestamp()), "exp": int((now + timedelta(minutes=10)).timestamp())}, PRIV_KEY1, "kid1")
    r = client.get("/protected", headers={"Authorization": f"Bearer {future}"})
    assert r.status_code == 401
    assert r.json()["code"] == "token_not_yet_valid"


def test_alg_and_kid_errors(tmp_path):
    app, _store, _path = build_app(tmp_path)
    client = TestClient(app)
    now = datetime.utcnow()
    hs_token = sign_hs({"sub": "u", "exp": int((now + timedelta(minutes=5)).timestamp())}, "secret")
    r = client.get("/protected", headers={"Authorization": f"Bearer {hs_token}"})
    assert r.status_code == 401
    assert r.json()["code"] == "invalid_alg"
    no_kid_header = {"alg": "RS256", "typ": "JWT"}
    hk = b64url(json.dumps(no_kid_header).encode())
    pk = b64url(json.dumps({"sub": "u", "exp": int((now + timedelta(minutes=5)).timestamp())}).encode())
    token_no_kid = sign({"sub": "u", "exp": int((now + timedelta(minutes=5)).timestamp())}, PRIV_KEY1, "kid1")
    # remove kid by rewriting header
    token_no_kid = token_no_kid.split('.')
    token_no_kid[0] = hk
    token_no_kid = '.'.join(token_no_kid)
    r = client.get("/protected", headers={"Authorization": f"Bearer {token_no_kid}"})
    assert r.status_code == 401
    assert r.json()["code"] == "missing_kid"
    unknown = sign({"sub": "u", "exp": int((now + timedelta(minutes=5)).timestamp())}, PRIV_KEY2, "kid2")
    r = client.get("/protected", headers={"Authorization": f"Bearer {unknown}"})
    assert r.status_code == 401
    assert r.json()["code"] == "unknown_kid"


def test_rotation(tmp_path):
    app, store, path = build_app(tmp_path)
    client = TestClient(app)
    data = yaml.safe_load(path.read_text())
    data["kid2"] = PUB_KEY2
    path.write_text(yaml.safe_dump(data))
    now = datetime.utcnow()
    token = sign({"sub": "u2", "tenant": "t2", "exp": int((now + timedelta(minutes=5)).timestamp())}, PRIV_KEY2, "kid2")
    r = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["sub"] == "u2"


def test_rejection_rate(tmp_path):
    app, _store, _path = build_app(tmp_path)
    client = TestClient(app)
    bad = "abc.def.ghi"
    rejected = 0
    for _ in range(100):
        r = client.get("/protected", headers={"Authorization": f"Bearer {bad}"})
        if r.status_code == 401:
            rejected += 1
    assert rejected >= 99


def test_no_token_leak(tmp_path, caplog):
    app, _store, _path = build_app(tmp_path)
    client = TestClient(app)
    now = datetime.utcnow()
    token = sign({"sub": "u", "exp": int((now - timedelta(minutes=2)).timestamp())}, PRIV_KEY1, "kid1")
    with caplog.at_level(logging.WARNING, logger="service.middleware.jwt"):
        client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert token not in caplog.text
    assert "jwt validation failed" in caplog.text
