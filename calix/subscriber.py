from requests import get

from calix.auth import username, password


def subs(e9, ont_id):
    subscriber = get(
        f"https://10.20.7.10:18443/rest/v1/config/device/{
            e9}/ontport/{ont_id}",
        auth=(username, password),
        verify=False,
    )
    return subscriber.json()
