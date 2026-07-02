from time import sleep
from netmiko import ConnectHandler

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
                "fast_cli": True,
            }
        else:
            self.ip = ip
            self.name = name
            self.device = {
                "device_type": "cisco_ios",
                "host": self.ip,
                "username": e9_user,
                "password": e9_pass,
                "fast_cli": True,
            }
        self.connection = ConnectHandler(**self.device)

    def backup(self, remote_path: str, passwd: str) -> None:
        cmds = [f"copy config from startup-config to {self.name}.xml\nupload file config from-file {self.name}.xml to-URI scp://{remote_path} password {passwd}"]
        run_cmds = self.connection.send_command_timing(cmds[0])
        return run_cmds

    def count_subs_port(self, port: str) -> int:
        run_cmds = int(self.connection.send_command(f"show int pon {port} subscriber-info | notab | inc subscriber-id | count").split()[1])
        return run_cmds

    @staticmethod
    def fiber_range(start: int, end: int, inc_12: bool = None):
        match inc_12:
            case None:
                fibers = (fiber for fiber in range(start, end + 1) if fiber % 12 != 0)
            case True:
                fibers = (fiber for fiber in range(start, end + 1))
        return fibers

    @staticmethod
    def pon_range(shelf: int, slot="", port="", odd=False, extend: list = None) -> list[str]:
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
        elif port != "":
            port_range = [port]
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

    def get_onts(self, ports: str | list) -> list[str]:
        """
        Params:
        port: str or list

        Description:
        Returns a set of all ONT ids on given port, if port is of type list, will return a single list of all ids from all ports in that list
        """
        if isinstance(ports, str):
            ont_ids = self.connection.send_command(f"show interface pon {ports} subscriber-info | csv | inc 17000".split(",")[1::5])
            return ont_ids
        elif isinstance(ports, list):
            ont_ids = []
            for port in ports:
                ont_ids.extend(self.connection.send_command(f"show interface pon {port} subscriber-info | csv | inc 17000").split(",")[1::5])
        else:
            raise TypeError
        return ont_ids

    def get_subs(self, onts: list, no_description=None, package=None) -> set:
        """
        Params:
        ont: list
        no_description: None optional
        package: None optional

        Pass in True value to the optional params to get their functionality
        """
        from calix.cx_detail import cx
        from calix.ont_detail import ont

        subscribers = set()
        for id in onts:
            cx_info = cx(self.name, id)
            if cx_info is None:
                continue
            ont_info = ont(self.name, id)
            name = cx_info.get("name")
            acct = cx_info.get("customId")
            phone = cx_info.get("locations")[0].get("contacts")[0].get("phone", "No phone")
            em = cx_info.get("locations")[0].get("contacts")[0].get("email", "No email")
            loc = f'{cx_info.get('locations')[0].get('address')[0].get('streetLine1', 'No location')},{cx_info.get('locations')[0].get('address')[0].get('city', 'No location')}'
            port = ont_info.get("linked-pon")
            fibers = CalixE9.description(self, port, "pon")
            pkg = self.connection.send_command(f"show running-config interface ont-ethernet {id}/x1 | inc policy-map").split()[1]
            match no_description:
                case True:
                    subscribers.add(f"{acct}\n{name}\n{phone}\n{em}\n{loc}\n")
                    continue
            match package:
                case True:
                    subscribers.add(f"{acct}\n{name}\n{phone}\n{em}\n{loc}\n{pkg}\n")
                    continue
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

        dying = self.connection.send_command("show alarm active | inc dying")
        match_ont = (search("'[0-9]{2,5}'", ont) for ont in dying.split("\n"))
        ont_ids = [m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None]
        return ont_ids

    def alrm_red_temp(self) -> list:
        from re import search

        red_temp = self.connection.send_command("show alarm active | inc red-temp")
        match_ont = (search("'[0-9]{2,5}'", ont) for ont in red_temp.split("\n"))
        ont_ids = [m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None]
        return ont_ids

    def alrm_missing(self) -> list:
        from re import search

        missing = self.connection.send_command("show alarm active | inc missing")
        match_ont = (search("'[0-9]{2,5}'", ont) for ont in missing.split("\n"))
        ont_ids = [m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None]
        return ont_ids

    def alrm_loss_of_pon(self) -> list:
        from re import search

        lop = self.connection.send_command("show alarm active | inc loss-of-pon")
        match_pon = [search("[2-5]/[1-2]/xp[0-9]{1,2}", port) for port in lop.split("\n") if "#" not in port]
        ports = [m.group() for m in match_pon]
        ont_ids = self.get_onts(ports)
        return ont_ids

    def alrm_maj(self) -> list:
        major = self.connection.send_command("show alarm active | inc MAJOR")
        return major.split("\n")

    def alrm_crit(self) -> list:
        critical = self.connection.send_command("show alarm active | inc CRITICAL")
        return critical.split("\n")

    def description(self, port: str, external: str) -> str:
        """
        External is the interface type
        ex: "pon", "ethernet", "lag", etc.
        """
        try:
            desc = self.connection.send_command(f"show running-config int {external} {port} | inc description").split()[1]
        except IndexError:
            return "No description"
        return desc

    def loss_of_signal(self) -> list:
        from re import search

        alarm = self.alrm_maj()
        m = (search("1/[1-2]/q[1-2]", port) for port in alarm if "loss-of-signal" in port)
        ports = [port.group() for port in m]
        return ports

    def pcap(self, interface: str, expr: str, remote_dst: str, filename: str):
        while True:
            print(self.connection.send_command_timing(f"tcpdump external-interface ont-ethernet {interface} file {filename} options {expr}", normalize=False))
            sleep(1)
