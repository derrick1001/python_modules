from netmiko import ConnectHandler


class CalixE9:
    def __init__(self, ip: str, name: str):
        self.ip = ip
        self.name = name
        self.device = {
            "device_type": "cisco_ios",
            "host": self.ip,
            "username": "sysadmin",
            "password": "Thesearethetimes!",
            "fast_cli": False,
        }
        self.connection = ConnectHandler(**self.device)

    def backup(self, remote_path: str, passwd: str) -> None:
        cmds = [
            f"copy config from startup-config to {self.name}.xml\nupload file config from-file {self.name}.xml to-URI scp://{remote_path} password {passwd}"
        ]
        run_cmds = self.connection.send_command_timing(cmds[0])
        return run_cmds

    def count_subs_port(self, port: str) -> int:
        cmd = f"show int pon {port} subscriber-info | notab | inc subscriber-id | count"
        run_cmds = int(
            self.connection.send_command_timing(cmd, strip_prompt=True).split()[1]
        )
        return run_cmds

    def ssp(self, shelf: str, slot="", port="") -> list[str]:
        if slot == "":
            slot_range = range(1, 3)
        else:
            slot_range = slot
        if "-" in port:
            port_range = range(int(port.split("-")[0]), int(port.split("-")[1]) + 1)
        else:
            port_range = range(1, 17)
        ranges = [
            f"{shelf}/{slot}/xp{port}" for slot in slot_range for port in port_range
        ]
        return ranges
