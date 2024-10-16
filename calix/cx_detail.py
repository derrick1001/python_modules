from requests import get


# NOTE: Returns dict of customer detail
def cx_detail(e9, ont_id):
    """
    This function requires the ONT id
    """
    cx = get(
        f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2Fx1",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return cx
