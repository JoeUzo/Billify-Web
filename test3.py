import os
import smtplib
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env if present

my_email = os.getenv("EMAIL")  # Your email address
password = os.getenv("EMAIL_KEY")  # Your app password

# Validate environment variables
if not my_email or not password:
    raise ValueError("EMAIL or EMAIL_KEY is not set in the .env file.")

try:
    # Connect to the Gmail SMTP server
    with smtplib.SMTP("smtp.gmail.com", port=587, timeout=60) as connection:
        connection.starttls()  # Upgrade the connection to secure
        connection.login(user=my_email, password=password)  # Login to the server
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Test\n\nThis is a test email from Windows!"
        )
    print("Email sent successfully!")

except smtplib.SMTPConnectError as e:
    print(f"Failed to connect to the SMTP server. Error: {e}")
    print("Make sure the network allows outbound connection to port 587.")
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication error: {e}")
    print("Ensure EMAIL and EMAIL_KEY are correct and App Passwords are enabled.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print("Check your environment or try again later.")
