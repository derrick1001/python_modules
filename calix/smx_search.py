from requests import get

from auth import username, password


def search_all(value: str):
    response = get(f"https://10.20.7.10:18443/rest/v1/es/search?_search={value}&offset=0&limit=20",
                   auth=(username, password),
                   verify=False,
                   )
    return response
