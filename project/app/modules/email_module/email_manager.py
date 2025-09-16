import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Union


class EmailManager:
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    is_production: bool

    def initialize(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        environment: str,
    ) -> None:
        """
        Initialize the client to database service
        :param smtp_host: smtp host
        :param smtp_port: smtp port
        :param smtp_user: smtp user
        :param smtp_password: smtp password
        :param environment: environment
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.is_production = environment == "pro"

    def _send_message(
        self,
        sender_user: str,
        receiver_user: Union[List[str], str],
        message_subject: str,
        message_body: MIMEText,
    ) -> None:
        """
        Send a message throughout smtp server
        :param sender_user: user that send the email
        :param receiver_user: list of users to send the email
        :param message_subject: subject of the message
        :param message_body: content of the message
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = (
            message_subject
            if self.is_production
            else f"QUA - {message_subject}"  # noqa: E501
        )
        message["From"] = sender_user
        message["To"] = receiver_user
        message.attach(message_body)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp_server:
            smtp_server.starttls(context=context)
            smtp_server.login(self.smtp_user, self.smtp_password)
            smtp_server.sendmail(
                sender_user, receiver_user, message.as_string()
            )  # noqa: E501

    def send_html_message(
        self,
        sender_user: str,
        receiver_user: Union[List[str], str],
        message_subject: str,
        message_text: str,
    ) -> None:
        """
        Send a message throughout smtp server
        :param sender_user: user that send the email
        :param receiver_user: list of users to send the email
        :param message_subject: subject of the message
        :param message_text: html text to send
        """
        self._send_message(
            sender_user,
            receiver_user,
            message_subject,
            MIMEText(message_text, "html"),  # noqa: E501
        )
