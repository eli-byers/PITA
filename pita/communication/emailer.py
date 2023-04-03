# Implements the send_email() function to send emails with the specified content after a given delay.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.config import EMAIL_ADDRESS, EMAIL_PASSWORD


def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        print(f"Email sent to {to_email} with subject: {subject}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Example usage
# send_email("recipient@example.com", "Test Subject", "Test email body")
