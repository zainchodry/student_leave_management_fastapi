import smtplib

from email.mime.text import MIMEText

from app.config import settings

def send_otp_email(
    receiver_email,
    otp
):

    subject = "Password Reset OTP"

    body = f"Your OTP is {otp}"

    message = MIMEText(body)

    message["Subject"] = subject

    message["From"] = settings.MAIL_FROM

    message["To"] = receiver_email

    server = smtplib.SMTP(
        settings.MAIL_SERVER,
        settings.MAIL_PORT
    )

    server.starttls()

    server.login(
        settings.MAIL_USERNAME,
        settings.MAIL_PASSWORD
    )

    server.sendmail(
        settings.MAIL_FROM,
        receiver_email,
        message.as_string()
    )

    server.quit()

