import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVICE_EMAIL = os.environ.get("SERVICE_EMAIL")
SERVICE_PASSWORD = os.environ.get("SERVICE_PASSWORD")


def send_mail(receiver_email,
              subject="[BOT] Esselunga's order confirmation",
              body="Your order has been successfully delivered"):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SERVICE_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SERVICE_EMAIL, SERVICE_PASSWORD)
        server.sendmail(SERVICE_EMAIL, receiver_email, message.as_string())
