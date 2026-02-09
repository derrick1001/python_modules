from requests import get

from auth import username, password


def cx(e9: str, ont_id: str) -> dict:
    """
    This function gets subscriber info using the ONT id

    Parameters
        e9: str
        ont_id: str

    Returns dictionary of all subscriber data if successfull
    """
    cx_detail = get(f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2Fx1",
                    auth=(username, password),
                    verify=False,
                    )
    if cx_detail.status_code == 200:
        return cx_detail.json()
    else:
        return
