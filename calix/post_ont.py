#!/usr/local/bin/python3.13

from requests import post

from calix.auth import username, password
from calix.server import SMX


def mk_ont(e9: str, **kwargs):
    ont = post(f"https://{SMX}:18443/rest/v1/config/device/{e9}/ont",
               auth=(username, password),
               verify=False,
               json=kwargs,
               )
    return ont
