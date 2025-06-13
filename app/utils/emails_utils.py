from email.message import EmailMessage

import aiosmtplib

from app.config.logger_config import func_logger
from app.config.settings import smtpsettings

SMTP_HOST = smtpsettings.SMTP_HOST
SMTP_PORT = smtpsettings.SMTP_PORT
SMTP_USER = smtpsettings.SMTP_USER
SMTP_PASS = smtpsettings.SMTP_PASS


async def send_verification_email(to_email: str, verification_link: str):
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = "Verify your Email"
    message.set_content(
        f"Click on the given link to verify your email:\n{verification_link}"
    )

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASS,
        )

        func_logger.info(f"Verification email sent to: {to_email}")

    except Exception as e:
        func_logger.exception(f"Failed to send verification link to: {to_email}")
