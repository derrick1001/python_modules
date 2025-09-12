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

    @staticmethod
    def ssp(shelf: str, slot="", port="") -> list[str]:
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

    def light(self, port: str) -> tuple[list, str]:
        from calix.cx_detail import cx
        from calix.ont_detail import ont
        from fiber_colors import ORANGE, GREEN, YELLOW, ROSE, AQUA

        ont_ids = self.connection.send_command_timing(
            f"sh int pon {port} ranged-onts statistics | inc ont-id"
        ).split()[1::2]
        module_len = self.connection.send_command_timing(
            f"show int pon {port} module | inc smf-fiber"
        ).split('"')[1]
        subs = []
        for onts in ont_ids:
            cx_info = cx(self.name, onts)
            ont_info = ont(self.name, onts)
            name = cx_info.get("name")
            sn = ont_info.get("serial-number")
            distance = ont_info.get("range-length")
            us_light = ont_info.get("ne-opt-signal-level")
            us_ber = ont_info.get("us-sdber-rate")
            subs.append(
                f"{AQUA}{sn}{YELLOW}{float(us_light):>10.2f}{YELLOW}{us_ber:>10}{GREEN}{distance / 1000:>10.1f}km{ROSE}{name:>30}\n"
            )
        return subs, f"{ORANGE}{module_len}"

    def alrm_maj(self) -> list:
        major = self.connection.send_command_timing("show alarm active | inc MAJOR")
        return major.split("\n")

    def alrm_crit(self) -> list:
        critical = self.connection.send_command_timing(
            "show alarm active | inc CRITICAL"
        )
        return critical.split("\n")

    def description(self, port: str) -> str:
        try:
            desc = self.connection.send_command_timing(
                f"show interface ethernet {port} status | include description",
                strip_prompt=True,
            ).split()[1]
        except IndexError:
            return "No description"
        return desc

    def loss_of_signal(self) -> list:
        from re import search

        alarm = self.alrm_maj()
        m = (
            search("1/[1-2]/q[1-2]", port) for port in alarm if "loss-of-signal" in port
        )
        ports = [port.group() for port in m]
        return ports
