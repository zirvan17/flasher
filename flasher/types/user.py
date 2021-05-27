from __future__ import annotations

import dataclasses

import requests


@dataclasses.dataclass
class User:
    userid: int
    shopid: int
    username: str
    email: str
    phone: str
    phone_verified: bool
    address: Address
    cookie: requests.sessions.RequestsCookieJar

    @dataclasses.dataclass
    class Address:
        address: str
        city: str
        country: str
        id_: int
        name: str
