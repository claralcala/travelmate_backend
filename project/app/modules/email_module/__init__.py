from .email_manager import EmailManager

__all__ = ["EmailModule", "register_email"]

EmailModule = EmailManager()


def register_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    environment: str,  # noqa: E501
) -> None:
    """
    Register email client in the application

    """
    global EmailModule
    EmailModule.initialize(
        smtp_host, smtp_port, smtp_user, smtp_password, environment
    )  # noqa: E501
