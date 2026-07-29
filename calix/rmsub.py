from requests import delete

from calix.auth import username, password
from calix.server import SMX


def rmsub(acct: str):
    rm_sub = delete(f"https://{SMX}:18443/rest/v1/ems/subscriber/org/Calix/account/{acct}",
                    auth=(username, password),
                    verify=False,
                    )
    return rm_sub.status_code
