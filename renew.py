import os
import requests

user = os.environ['user'].split(';')
session = requests.session()
login = session.post("https://iray.club/api/v1/passport/auth/login", data={
    "email": user[0],
    "password": user[1]
})
if login.status_code != 200:
    exit(login.status_code)


def get_link() -> str:
    subscribe = session.get("https://iray.club/api/v1/user/getSubscribe")
    return subscribe.json()["data"]["subscribe_url"]


def change_link() -> str:
    reset = session.get("https://iray.club/api/v1/user/resetSecurity")
    return reset.json()["data"]

change_link()

