from calix.rmont import rmont
from calix.rmsub import rmsub


def rem_sub(accounts: list):
    for acct in accounts:
        delete = rmsub(acct)
        if delete == 200:
            print("Account removed successfully!!")
        elif delete == 404:
            print(f"Account {acct} id not exist, skipping")
            continue


def rem_ont(id_e9: dict):
    for id, e9 in id_e9.items():
        remove = rmont(id, e9)
        if remove == 200:
            print("ONT removed successfully!!")
        elif remove == 404:
            print(f"ONT {id} did not exist, skipping")
            continue
