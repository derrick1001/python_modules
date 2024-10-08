#!/usr/bin/python3

from sys import argv
from netmiko import ConnectHandler
from requests import get


def cx_detail(e9, ont_id):
    response = get(
        f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2Fx1",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return response


def ssp():
    from crayon import c_BLUE, c_WHITE

    shelf = input(f"{c_BLUE}Shelf: {c_WHITE}")
    slot = input(f"{c_BLUE}Slot: {c_WHITE}")
    port = input(f"{c_BLUE}Port: {c_WHITE}")
    print("")
    return shelf, slot, port


def netcon(shelf, slot, port):
    device = {
        "device_type": "cisco_ios",
        "host": f"{argv[1]}",
        "username": "sysadmin",
        "password": "Thesearethetimes!",
        "fast_cli": False,
    }
    return ConnectHandler(**device)


if __name__ == "__main__":
    pass
