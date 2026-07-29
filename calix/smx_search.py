from requests import get

from calix.auth import username, password
from server import SMX


def search_all(value: str):
    response = get(f"https://{SMX}:18443/rest/v1/es/search?_search={value}&offset=0&limit=20",
                   auth=(username, password),
                   verify=False,
                   )
    return response
