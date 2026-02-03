#!/usr/local/bin/python3.13

from requests import post

from calix.auth import username, password


def mk_ont(e9: str, **kwargs):
    ont = post(
        f"https://10.20.7.10:18443/rest/v1/config/device/{e9}/ont",
        auth=(username, password),
        verify=False,
        json=kwargs,
    )
    return ont
