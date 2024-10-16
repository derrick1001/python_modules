from requests import get


# NOTE: Returns dict of ont detail
def ont_detail(e9, ont_id):
    ont = get(
        f"https://10.20.7.10:18443/rest/v1/performance/device/{e9}/ont/{ont_id}/status",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return ont
