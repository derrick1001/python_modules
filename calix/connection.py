from sys import argv
from netmiko import ConnectHandler

from calix.auth import e9_user, e9_pass


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
        "username": e9_user,
        "password": e9_pass,
        "fast_cli": False,
    }
    return ConnectHandler(**device)
