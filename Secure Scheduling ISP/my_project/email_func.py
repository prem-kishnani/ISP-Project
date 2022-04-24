import smtplib, ssl
from email.mime.text import MIMEText

def email_verification(receiver_email):
    port = 465
    password = input("Type your password and press enter:")
    smtp_server = "smtp.gmail.com"
    sender_email = "pkishnaniisp@gmail.com"
    message = """\n
    Subject: Hi there

    This message is sent from Python. Thank you for registering. You can log into your account on the Secure Scheduler and view your schedule. If you're a new user, you can also input your schedule there."""


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,receiver_email,message)
