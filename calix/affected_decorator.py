from calix.cx_detail import cx
from calix.fibers import get_fibers
from calix.pon_ports import get_pon_ports


def affected_decorator(func):
    def inner(*args, **kwargs):
        ont_ids = func()
        pon_ports = get_pon_ports(ont_ids, kwargs.get("e9"))
        fibers = get_fibers(pon_ports)
        pon_ports = (port for port in pon_ports)
        account = (cx(kwargs.get("e9"), id) for id in ont_ids if id is not None)
        for sub in account:
            try:
                name = sub.get("name")
                acct = sub.get("customId")
                phone = sub.get("locations")[0].get("contacts")[0].get("phone")
                em = sub.get("locations")[0].get("contacts")[0].get("email")
                loc = (
                    sub.get("locations")[0].get("address")[0].get("streetLine1")
                    + ", "
                    + sub.get("locations")[0].get("address")[0].get("city")
                )
                fiber = next(fibers)
            except Exception:
                if name or acct is None:
                    continue
            except IndexError:
                fiber = "Not configured"
            else:
                if phone is None or phone == "":
                    phone = "No phone"
                if em is None or em == "":
                    em = "No email"
                if loc is None or loc == "":
                    loc = "No location"
                port = next(pon_ports)
            yield f"{acct}\n{name}\n{phone}\n{port}_{fiber}\n{em}\n{loc}\n"

    return inner
