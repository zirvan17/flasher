from __future__ import annotations

import enum
import hashlib
import random
import string
import typing as t

import requests
from . import _urls


class Login:
    session: requests.Session
    user: str
    user_type: str

    @staticmethod
    def init(user: str, password: str) -> t.Tuple[t.Optional[Login], bool]:
        self = Login()
        self.session, self.user = requests.Session(), user

        self.session.cookies.set("csrftoken", Login.randomize_token())
        self.session.headers.update({
            "referer": _urls.PREFIX,
            "if-none-match-": "*",
            "x-csrftoken": self.session.cookies.get("csrftoken"),
            "user-agent": "Android app Shopee appver\u003d26921 app_type\u003d1"
        })
        self.session.post("https://shopee.co.id/buyer/login")
        self.user_type = {
                "@" in user: "email",
                user.isdigit(): "phone"
            }.get(True, "username")
        password = hashlib.md5(password.encode()).hexdigest()
        password = hashlib.sha256(password.encode()).hexdigest()
        resp = self.session.post(_urls.PREFIX + _urls.PATHS["auth_login"],
                                 json={
                                     self.user_type: user,
                                     "password": password,
                                     "support_ivs": True,
                                     "support_whats_app": True
                                 })
        data = resp.json()

        if data["error"] != 77:
            # login error
            return None, False

        return self, self.session.cookies.get("SPC_U") != "-"

    def send_otp(self, channel: OTPChannel) -> Login:
        self.session.post(_urls.PREFIX + _urls.PATHS["auth_otp"],
                          json={
                              "channel": channel.value,
                              "force_channel": True,
                              "operation": 5,
                              "support_whats_app": True
                          })

        return self

    def verify(self, code: str) -> t.Optional[requests.sessions.RequestsCookieJar]:
        resp = self.session.post(_urls.PREFIX + _urls.PATHS["auth_vcode"],
                                 json={
                                     "otp": code,
                                     self.user_type: self.user,
                                     "support_ivs": True
                                 })
        data = resp.json()

        if data["error"] is None:
            return self.session.cookies

    @staticmethod
    def randomize_token() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    class OTPChannel(enum.Enum):
        WHATSAPP = 3
        SMS = 1
        CALL = 2
