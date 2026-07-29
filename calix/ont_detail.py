from requests import get

from calix.auth import username, password
from calix.server import SMX


def ont(e9: str, ont_id: str):
    """
    This function gets ONT detail using the ONT id

    Parameters
        e9: str
        ont_id: str

    Returns dictionary of all ONT data
    """
    ont_detail = get(f"https://{SMX}:18443/rest/v1/performance/device/{e9}/ont/{ont_id}/status",
                     auth=(username, password),
                     verify=False)
    if isinstance(ont_detail.json(), list):
        return "ONT does not exist"
    elif isinstance(ont_detail.json(), dict):
        return ont_detail.json()
