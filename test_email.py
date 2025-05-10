import smtplib
from email.mime.text import MIMEText
import environ
from dotenv import load_dotenv
import os



# Replace with your actual email and app password
load_dotenv()  # Load environment variables from a .env file
sender_email ='sonupal0840@gmail.com ' # Use environment variable for email username

receiver_email = "sonustar0840@gmail.com"
password = 'zwxr akji ujoo qgin' # The application-specific password

# Compose the email
msg = MIMEText("This is a test email.")
msg["Subject"] = "Test Email"
msg["From"] = sender_email
msg["To"] = receiver_email

# Send the email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
    print("Failed to send email.")