from requests import get


def ont(e9, ont_id):
    """
    This function gets ONT detail using the ONT id

    Parameters
        e9: str
        ont_id: str

    Returns dictionary of all ONT data
    """
    ont_detail = get(
        f"https://10.20.7.10:18443/rest/v1/performance/device/{e9}/ont/{ont_id}/status",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return ont_detail.json()
