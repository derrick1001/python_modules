from requests import get

from calix.cx_detail import cx
from calix.auth import username, password
from calix.server import SMX

# NOTE:
# This is the 'Subscribers' hyperlink under alarms
# This will show a good amount of information on the affected subscriber


def affected(e9, instid):
    response = get(f"https://{SMX}:18443/rest/v1/fault/export/csv/subscriber/device-name/{e9}/instance-id/{id}",
                   auth=(username, password),
                   verify=False,
                   )
    return response
