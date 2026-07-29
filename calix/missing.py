from requests import get

from auth import username, password
from server import SMX


def missing(e9):
    miss_ont = get(
        f"https://{SMX}:18443/rest/v1/config/device/{
            e9}/ont/missingONTs?offset=0&limit=20",
        auth=(username, password),
        verify=False,
    )
    return miss_ont
