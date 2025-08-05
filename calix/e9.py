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
        cmds = (
            f"show int pon {port} subscriber-info | notab | inc subscriber-id | count"
        )
        run_cmds = int(
            self.connection.send_command_timing(cmds, strip_prompt=True).split()[1]
        )
        return run_cmds
