from calix.cx_detail import cx
from calix.affected import affected
from calix.path import cvec_alrms

# NOTE:
#   Debating on what to do once code is churned through this
#   decorator. Write to file and reuse later?


def affected_decorator(func):
    def inner(*args, **kwargs):
        account = (affected(args[0], id).text.split("\r\n")[1:-1] for id in args[1])
        try:
            for sub, id in zip(account, args[2]):
                r1 = cx(args[0], id)
        except IndexError:
            try:
                phone = r1.get("locations")[0].get("contacts")[0].get("phone")
                if phone is None:
                    phone = "No phone"
            except Exception:
                phone = "No phone"
            splt_i = sub[0].split(",")
            acct, name, loc, em = (
                splt_i[0],
                splt_i[1],
                " ".join(splt_i[2:5]),
                splt_i[-1],
            )
            if em == "":
                em = "No email"
            print(f"{acct}\n{name}\n{phone}\n{em}\n{loc}\n")
        return

    return inner
