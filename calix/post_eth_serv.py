from requests import post


def mk_eth_serv(**kwargs):
    eth_serv = post(
        "https://10.20.7.10:18443/rest/v1/ems/service",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
        json=kwargs,
    )
    return eth_serv
