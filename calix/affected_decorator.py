from calix.cx_detail import cx
from calix.pon_ports import get_pon_fibers


def affected_decorator(func):
    """
    This function parses out the list or lists of
    ids from the proc_alarms function

    Parameters
        decorator function

    Yields an f-string of the subscriber data
    """

    def inner(*args, **kwargs):
        ont_ids = func()
        subs = set()
        for ont in ont_ids:
            pon_ports, fibers = get_pon_fibers(ont, kwargs.get("e9"))
            account = (cx(kwargs.get("e9"), id) for id in ont if id is not None)
            for sub in account:
                try:
                    name = sub.get("name")
                    acct = sub.get("customId")
                    phone = sub.get("locations")[0].get("contacts")[0].get("phone")
                    em = sub.get("locations")[0].get("contacts")[0].get("email")
                    loc = (sub.get("locations")[0].get("address")[0].get("streetLine1")+ ", "+ sub.get("locations")[0].get("address")[0].get("city"))
                except Exception:
                    if name or acct is None:
                        continue
                else:
                    if phone is None or phone == "":
                        phone = "No phone"
                    if em is None or em == "":
                        em = "No email"
                    if loc is None or loc == "":
                        loc = "No location"
                    port = next(pon_ports)
                    fiber = next(fibers)
                subs.add(f"{acct}\n{name}\n{phone}\n{port} -> {fiber}\n{em}\n{loc}\n")
        for sub in subs:
            yield sub

    return inner
