import smtplib
import ssl
import getpass
import socket
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class SendEmail:
    sender_email = "brandonsbiggsdev@gmail.com"
    port = 465  # For SSL
    password = os.environ['app_password']
    receiver_email = "biggbran@isu.edu"

    def __init__(self, message, subject="Code Results"):
        self.hostname = socket.gethostname()
        self.current_datetime = str(datetime.datetime.now())
        # self.password = getpass.getpass("Password:")
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = subject + " " + self.hostname + " " + self.current_datetime
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self._setup_message(message)

    def _setup_message(self, message):
        # Create the plain-text and HTML version of your message
        text = """\
        Results from {0} at {1}:
        {2}"""
        html = """\
        <html>
          <body>
            <p>Results from {0} at {1}: <br> {2}
            </p>
          </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text.format(
            self.hostname,                  # {0}
            self.current_datetime,          # {1}
            message,                        # {2}
        ), "plain")
        part2 = MIMEText(html.format(
            self.hostname,                  # {0}
            self.current_datetime,          # {1}
            message,                        # {2}
        ), "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        self.message.attach(part1)
        self.message.attach(part2)

    def send_email(self):
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
        self.password = ""
