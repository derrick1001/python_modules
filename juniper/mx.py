from netmiko import ConnectHandler


class MX:
    def __init__(self, ip: str, name: str):
        self.ip = ip
        self.name = name
        self.device = {
            "device_type": "juniper_junos",
            "host": self.ip,
            "username": "derrick",
            "use_keys": True,
            "key_file": "/home/derrick/.ssh/cvec_ed25519",
            "fast_cli": False,
        }
        self.connection = ConnectHandler(**self.device)
