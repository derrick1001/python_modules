import smtplib
from email.message import EmailMessage


def email(subj: str, cont) -> None:
    msg = EmailMessage()
    msg.set_content(cont)
    msg["Subject"] = subj
    msg["From"] = "nms@mycvecfiber.com"
    msg["To"] = "dishman@cvecfiber.com"
    if "PON" not in subj:
        msg["Cc"] = [
            "kmarshala@cvecfiber.com",
            "jjackson@cvecfiber.com",
            "jailey@cvecfiber.com",
        ]
    s = smtplib.SMTP("10.20.17.31")
    s.send_message(msg)
    s.quit()
