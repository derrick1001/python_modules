from netmiko import ConnectHandler
from sys import argv


# NOTE: Returns connection object
def calix_e9():
    device = {
        "device_type": "cisco_ios",
        "host": f"{argv[1]}",
        "username": "sysadmin",
        "password": "Thesearethetimes!",
        "fast_cli": False,
    }
    return ConnectHandler(**device)
