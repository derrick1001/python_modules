#!/usr/local/bin/python3.13

from requests import post


def mk_ont(e9: str, **kwargs):
    mk_ont = post(
        "https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
        json=kwargs,
    )
