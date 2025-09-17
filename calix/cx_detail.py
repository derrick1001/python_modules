from requests import get


def cx(e9, ont_id):
    """
    This function gets subscriber info using the ONT id

    Parameters
        e9: str
        ont_id: str

    Returns dictionary of all subscriber data
    """
    cx_detail = get(
        f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2Fx1",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    if cx_detail.status_code == 200:
        return cx_detail.json()
    else:
        return
    # cx_detail = get(
    #    f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2FG1",
    #    auth=("admin", "Thesearethetimes!"),
    #    verify=False,
    # )
