from requests import post

from calix.auth import username, password


def mk_eth_serv(**kwargs):
    eth_serv = post("https://10.20.7.10:18443/rest/v1/ems/service",
                    auth=(username, password),
                    verify=False,
                    json=kwargs,
                    )
    return eth_serv
