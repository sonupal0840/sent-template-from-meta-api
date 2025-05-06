# leads/utils.py

import smtplib
from email.message import EmailMessage

def send_email(to_email):
    msg = EmailMessage()
    msg['Subject'] = 'Thank You for Your Interest'
    msg['From'] = 'sonustar0840@gmail.com'
    msg['To'] = to_email
    msg.set_content('We appreciate your interest. Our team will follow up shortly.')

    # SMTP Setup
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('sonustar0840@gmail.com', 'lvck icrg qujw hdib')  # Use App Password, not your real password
    server.send_message(msg)
    server.quit()
