from calix.cx_detail import cx

# NOTE:
#   This decorator takes in an iterable and calls
#   cx function from calix.cx_detail to put together
#   our own affected subscriber output


def affected_decorator(func):
    def inner(*args, **kwargs):
        ont_ids = func()
        account = (cx(kwargs.get('e9'), id) for id in ont_ids)
        for sub in account:
            try:
                name = sub.get("name")
                if name is None:
                    continue
            except Exception:
                pass
            try:
                phone = sub.get("locations")[0].get("contacts")[0].get("phone")
            except Exception:
                phone = "No phone"
            else:
                if phone is None:
                    phone = "No phone"
            try:
                em = sub.get("locations")[0].get("contacts")[0].get("email")
            except Exception:
                em = "No email"
            else:
                if em is None:
                    em = "No email"
            try:
                loc = sub.get("locations")[0].get("address")[0].get(
                    "streetLine1") + ', ' + sub.get("locations")[0].get("address")[0].get("city")
            except Exception:
                loc = 'No address'
            acct = sub.get("customId")
            print(f"{acct}\n{name}\n{phone}\n{em}\n{loc}\n")
        return

    return inner
