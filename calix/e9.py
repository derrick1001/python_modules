from netmiko import ConnectHandler
from typing import Union

from calix.auth import e9_pass, e9_user


class CalixE9:
    def __init__(self, ip: str | tuple[str, str], name: str | None = None):
        if name is None:
            IP, NAME = ip
            self.ip = IP
            self.name = NAME
            self.device = {
                "device_type": "cisco_ios",
                "host": self.ip,
                "username": e9_user,
                "password": e9_pass,
                "fast_cli": False,
            }
        else:
            self.ip = ip
            self.name = name
            self.device = {
                "device_type": "cisco_ios",
                "host": self.ip,
                "username": e9_user,
                "password": e9_pass,
                "fast_cli": False,
            }
        self.connection = ConnectHandler(**self.device)

    def backup(self, remote_path: str, passwd: str) -> None:
        cmds = [f"copy config from startup-config to {self.name}.xml\nupload file config from-file {self.name}.xml to-URI scp://{remote_path} password {passwd}"]
        run_cmds = self.connection.send_command_timing(cmds[0])
        return run_cmds

    def count_subs_port(self, port: str) -> int:
        cmd = f"show int pon {port} subscriber-info | notab | inc subscriber-id | count"
        run_cmds = int(self.connection.send_command_timing(cmd, strip_prompt=True).split()[1])
        return run_cmds

    @staticmethod
    def fiber_range(start: int, end: int, inc_12: bool = None):
        if inc_12 is None:
            fibers = (fiber for fiber in range(start, end + 1) if fiber % 12 != 0)
        elif inc_12 is True:
            fibers = (fiber for fiber in range(start, end + 1))
        return fibers

    @staticmethod
    def pon_range(shelf: str, slot="", port="", odd=False, extend=None) -> list[str]:
        """
        Params:
        shelf: int 1-5
        slot: str 1-2
        port: str 1-32
        odd: bool (default=False)
        extend: list

        When calling ssp, use an empty string for slot if you need a range across both slots

        odd=True - Returns given range with step 2
        extend=list - adds this list to the original list before returning (ex: ranges += extend)
        """
        if slot == "":
            slot_range = range(1, 3)
        else:
            slot_range = slot
        if "-" in port and odd is False:
            port_range = range(int(port.split("-")[0]), int(port.split("-")[1]) + 1)
        elif "-" and odd is True:
            port_range = range(int(port.split("-")[0]), int(port.split("-")[1]) + 1, 2)
        else:
            port_range = range(1, 17)
        ranges = [f"{shelf}/{slot}/xp{port}" for slot in slot_range for port in port_range]
        if extend is not None:
            ranges += extend
            return ranges
        else:
            return ranges

    @staticmethod
    def eth_range(eth_type: str, slot="", port="") -> list[str]:
        """
        Params:
        eth_type: "q", "g", "x"
        slot: str 1-2
        port: str 1-9
        """
        shelf = 1
        if slot == "":
            slot_range = range(1, 3)
        else:
            slot_range = slot
        if "-" in port:
            port_range = range(int(port.split("-")[0]), int(port.split("-")[1]) + 1)
        else:
            match eth_type:
                case "x":
                    port_range = range(1, 9)
                case "g" | "q":
                    port_range = range(1, 3)
        ranges = [f"{shelf}/{slot}/{eth_type}{port}"for slot in slot_range for port in port_range]
        return ranges

    def get_onts_on_port(self, port: Union[str, list]) -> list[str]:
        """
        Params:
        port: str or list

        Description:
        Returns a list of all ONT ids on given port, if port is of type list, will return a single list of all ids from all ports in that list
        """
        if isinstance(port, str):
            ont_ids = self.connection.send_command_timing(f"show interface pon {port} ranged-onts statistics | inc ont-id").split()[1::2]
        elif isinstance(port, list):
            ont_ids = []
            for ports in port:
                ont_ids.extend(self.connection.send_command_timing(f"show interface pon {ports} ranged-onts statistics | inc ont-id").split()[1::2])

        else:
            TypeError
        return ont_ids

    def get_subs(self, onts: list) -> set:
        from calix.cx_detail import cx
        from calix.ont_detail import ont

        subscribers = set()
        for id in onts:
            cx_info = cx(self.name, id)
            if cx_info is None:
                continue
            ont_info = ont(self.name, id)
            try:
                name = cx_info.get("name")
                acct = cx_info.get("customId")
                phone = cx_info.get("locations")[0].get("contacts")[0].get("phone")
                em = cx_info.get("locations")[0].get("contacts")[0].get("email")
                loc = (cx_info.get("locations")[0].get("address")[0].get("streetLine1") + ", " + cx_info.get("locations")[0].get("address")[0].get("city"))
            except TypeError:
                pass
            else:
                if phone is None or phone == "":
                    phone = "No phone"
                if em is None or em == "":
                    em = "No email"
                if loc is None or loc == "":
                    loc = "No location"
            port = ont_info.get("linked-pon")
            self.connection.send_command_timing("configure")
            fibers = CalixE9.description(self, port, "pon")
            subscribers.add(f"{acct}\n{name}\n{phone}\n{port} -> {fibers}\n{em}\n{loc}\n")
        return subscribers

    def light(self, port: str) -> tuple[list, str]:
        from calix.cx_detail import cx
        from calix.ont_detail import ont
        from fiber_colors import PEACH, GREEN, YELLOW, SKY, RED, MAROON

        ont_ids = self.connection.send_command_timing(f"sh int pon {port} ranged-onts statistics | inc ont-id").split()[1::2]
        module_len = self.connection.send_command_timing(f"show int pon {port} module | inc smf-fiber").split('"')[1]
        subs = []
        for onts in ont_ids:
            cx_info = cx(self.name, onts)
            try:
                name = cx_info.get("name")
            except AttributeError:
                continue
            ont_info = ont(self.name, onts)
            name = cx_info.get("name")
            sn = ont_info.get("serial-number")
            distance = ont_info.get("range-length")
            us_light = ont_info.get("ne-opt-signal-level")
            try:
                float(us_light)
            except ValueError:
                us_light = 0.00
            us_ber = ont_info.get("us-sdber-rate")
            us_err = ont_info.get("us-bip-errors")
            subs.append(f"{MAROON}{sn}{YELLOW}{float(us_light):>10.2f}{YELLOW}{us_ber:>10}{GREEN}{distance / 1000:>10.1f}km{RED}{us_err:>10}{SKY}{name:>30}\n")
        return subs, f"{PEACH}{module_len}"

    def alrm_dying(self) -> list:
        from re import search

        dying = self.connection.send_command_timing("show alarm active | inc dying")
        match_ont = (search("'[0-9]{2,5}'", ont) for ont in dying.split("\n"))
        ont_ids = [m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None]
        return ont_ids

    def alrm_missing(self) -> list:
        from re import search

        missing = self.connection.send_command_timing("show alarm active | inc missing")
        match_ont = (search("'[0-9]{2,5}'", ont) for ont in missing.split("\n"))
        ont_ids = [m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None]
        return ont_ids

    def alrm_maj(self) -> list:
        major = self.connection.send_command_timing("show alarm active | inc MAJOR")
        return major.split("\n")

    def alrm_crit(self) -> list:
        critical = self.connection.send_command_timing("show alarm active | inc CRITICAL")
        return critical.split("\n")

    def description(self, port: str, external: str) -> str:
        """
        External is the interface type
        ex: "pon", "ethernet", "lag", etc.
        """
        try:
            self.connection.send_command_timing("configure")
            desc = self.connection.send_command_timing(f"show full int {external} {port} | inc description", strip_prompt=True).split()[1]
        except IndexError:
            return "No description"
        return desc

    def loss_of_signal(self) -> list:
        from re import search

        alarm = self.alrm_maj()
        m = (search("1/[1-2]/q[1-2]", port) for port in alarm if "loss-of-signal" in port)
        ports = [port.group() for port in m]
        return ports
