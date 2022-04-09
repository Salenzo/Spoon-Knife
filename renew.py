from nacl import encoding, public
from base64 import b64encode
import os
import requests


def get_link() -> str:
    subscribe = session.get("https://iray.club/api/v1/user/getSubscribe")
    return subscribe.json()["data"]["subscribe_url"]


def change_link() -> str:
    reset = session.get("https://iray.club/api/v1/user/resetSecurity")
    return reset.json()["data"]


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(
        public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


user = os.environ['user'].split(';')
session = requests.session()
login = session.post("https://iray.club/api/v1/passport/auth/login", data={
    "email": user[0],
    "password": user[1]
})
if login.status_code != 200:
    exit(login.status_code)
link = change_link()

