from netmiko import ConnectHandler

from juniper.auth import username, key_file


class MX:
    def __init__(self, ip: str, name: str):
        self.ip = ip
        self.name = name
        self.device = {
            "device_type": "juniper_junos",
            "host": self.ip,
            "username": username,
            "use_keys": True,
            "key_file": key_file,
            "fast_cli": False,
        }
        self.connection = ConnectHandler(**self.device)
