import os
from dotenv import load_dotenv
import smtplib

load_dotenv()


class Mail:

    def __init__(self, data):
        self.data = data
        self.my_email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_KEY")

        self.mail = f"Name: {self.data['name']}\nEmail: {self.data['email']}\n" \
                    f"Phone No.: {self.data['phone']}\nMessage: {self.data['message']}"

        self.send_mail()

    def send_mail(self):

        # mail = f"Name: {self.data['name']}\nEmail: {self.data['email']}\n" \
        #        f"Phone No.: {self.data['phone']}\nMessage: {self.data['message']}"

        # Validate environment variables
        if not self.my_email or not self.password:
            raise ValueError("EMAIL or EMAIL_KEY is not set in the .env file.")


        try:
            with smtplib.SMTP("smtp.gmail.com", port=587, timeout=60) as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.password)
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=self.my_email,
                    msg=f"subject: BILLIFY\n\n{self.mail}".encode('utf-8')
                )

        except smtplib.SMTPConnectError as e:
            print(f"Failed to connect to the SMTP server. Error: {e}")
            print("Make sure the network allows outbound connection to port 587.")
        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication error: {e}")
            print("Ensure EMAIL and EMAIL_KEY are correct and App Passwords are enabled.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Check your environment or try again later.")