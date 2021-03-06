import smtplib, ssl
from utils.config import email_password

def send_email(email, name, new_password):
    
    query_email = "memorylane.297@gmail.com"
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "memorylane.297@gmail.com"
    receiver_email = email
    password = email_password
    message = f"""\
    Subject: Password recovery.
    Hello {name},
    New password has been set successfully for your account on Compra-Venta.
    For any queries contact {query_email}.
    New Password : {new_password}
    """

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        try:
            server.sendmail(sender_email, receiver_email, message)
            return True
        except:
            return False