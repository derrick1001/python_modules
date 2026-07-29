from requests import post

from calix.auth import username, password
from calix.server import SMX


def mk_eth_serv(**kwargs):
    eth_serv = post("https://{SMX}:18443/rest/v1/ems/service",
                    auth=(username, password),
                    verify=False,
                    json=kwargs,
                    )
    return eth_serv
