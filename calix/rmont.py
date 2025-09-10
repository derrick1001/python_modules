#!/usr/local/bin/python3.13

from requests import delete


def rmont(id: str, e9: str):
    """
    API DELETE method that deletes the given ONT id

    Parameters: id: str, e9: str

    Returns nothing
    """

    del_ont = delete(
        f"https://10.20.7.10:18443/rest/v1/config/device/{e9}/ont?ont-id={id}&force-delete=true",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return del_ont.status_code, del_ont.json()
