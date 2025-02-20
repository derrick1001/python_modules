import re

from calix.affected_decorator import affected_decorator
from calix.connection import calix_e9


def proc_alarms(func):
    """
    This function processes the alarm table
    by matching the pon port or ONT id
    from the alarm and making a data
    structure from it

    Parameters
        This is a decorator function and
        takes in another function as its arg

    Returns a generator object of list or lists or ids
    """

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
                    f"show interface pon {
                        port} subscriber-info | display curly-braces | inc ont-id",
                )
                for port in pon_port
            )
            ont_ids = [id.rstrip(";") for id in next(sub_on_port).split()[1::2]]
            yield ont_ids
        else:
            match_ont = [
                re.search("'[0-9]{3,5}'", alrm) for alrm in alrm_tbl.split("\n")
            ]
            ont_ids = [
                m.group().lstrip("'").rstrip("'") for m in match_ont if m is not None
            ]
            yield ont_ids

    return inner
