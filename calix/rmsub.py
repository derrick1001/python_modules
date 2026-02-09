from requests import delete

from auth import username, password


def rmsub(acct: str):
    rm_sub = delete(f"https://10.20.7.10:18443/rest/v1/ems/subscriber/org/Calix/account/{acct}",
                    auth=(username, password),
                    verify=False,
                    )
    return rm_sub.status_code
