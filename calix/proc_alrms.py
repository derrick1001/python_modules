import re

from calix.affected_decorator import affected_decorator
from calix.connection import calix_e9


def proc_alarms(func):
    @affected_decorator
    def inner(**kwargs):
        alrm_tbl = func()
        if "loss-of-pon" in alrm_tbl:
            match_pon = (
                re.search("[2-5]/[1-2]/xp[0-9]{1,2}", alrm)
                for alrm in alrm_tbl.split("\n")
            )
            pon_port = (
                m.group().lstrip("'").rstrip("'") for m in match_pon if m is not None
            )
            cnct = calix_e9()
            sub_on_port = (
                cnct.send_command_timing(
                    f"show interface pon {port} subscriber-info | display curly-braces | inc ont-id",
                    strip_prompt=True,
                )
                for port in pon_port
            )
            pattern = re.compile(r"[0-9]{3,5}")
            ont_id = (pattern.findall(id) for id in sub_on_port)
            return ont_id
        else:
            match_ont = [
                re.search("'[0-9]{1,5}'", alrm) for alrm in alrm_tbl.split("\n")
            ]
            ont_id = [
                m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None
            ]
            return ont_id

    return inner
