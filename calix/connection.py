from sys import argv
from netmiko import ConnectHandler

from calix.auth import username, password


# NOTE: Returns connection object
def calix_e9():
    """
    This function sets up a
    common ssh connection to
    the device it was called with.

    Parameters:
        Called with ip address

    It returns the connection
    object that you can call
    in the script.
    """
    device = {
        "device_type": "cisco_ios",
        "host": f"{argv[1]}",
        "username": username,
        "password": password,
        "fast_cli": False,
    }
    return ConnectHandler(**device)
