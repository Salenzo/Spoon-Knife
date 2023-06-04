from nacl import encoding, public
from base64 import b64encode
import os
import requests
import json


def get_link() -> str:
    subscribe = session.get(os.environ['baseUrl'] + "api/v1/user/getSubscribe")
    return subscribe.json()["data"]["subscribe_url"]


def change_link() -> str:
    reset = session.get(os.environ['baseUrl'] + "api/v1/user/resetSecurity")
    return reset.json()["data"]


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(
        public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

# dg lu
user = os.environ['user'].split(';')
session = requests.session()
login = session.post(os.environ['baseUrl'] + "api/v1/passport/auth/login", data={
    "email": user[0],
    "password": user[1]
})

token = os.environ['token']
public_key = json.loads(requests.get("https://api.github.com/repos/Salenzo/Spoon-Knife/actions/secrets/public-key", headers={
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}).content)

# yi ih, is xn ho qu baseUrl
if login.status_code != 200:
    from bs4 import BeautifulSoup
    response = requests.get("https://xn--zuup71g88ae4i.com/")
    soup = BeautifulSoup(response.content, "html.parser")
    for a in soup.find_all("a"):
        if a.text.strip().startswith("立即进入"):
            print(a.href)
            baseUrl = a.href
    print(requests.put("https://api.github.com/repos/Salenzo/Spoon-Knife/actions/secrets/BASE_URL", headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }, data=json.dumps({
        "key_id": public_key["key_id"],
        "encrypted_value": encrypt(public_key["key"], baseUrl)
    })).content, "gg xn baseUrl")
    exit(login.status_code)

"""os.environ['url'] = change_link()"""  # 这个只会影响当前进程，py退出后就没了
"""
url = change_link()

# gg xn
print(requests.put("https://api.github.com/repos/Salenzo/Spoon-Knife/actions/secrets/URL", headers={
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
}, data=json.dumps({
    "key_id": public_key["key_id"],
    "encrypted_value": encrypt(public_key["key"], url)
})).content, "xiu gai mi mi")
"""
print(requests.post("https://api.github.com/repos/Salenzo/Spoon-Knife/actions/workflows/ruby.yml/dispatches", headers={
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
}, data=json.dumps({
    "ref": "main", "inputs": {}
})).content, "shua xin ding yue")
