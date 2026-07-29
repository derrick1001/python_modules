from requests import get

from auth import username, password
from server import SMX


def subs(e9, ont_id):
    subscriber = get(f"https://{SMX}:18443/rest/v1/config/device/{e9}/ontport/{ont_id}",
                     auth=(username, password),
                     verify=False,
                     )
    return subscriber.json()
