from tortoise import fields

from app.modules.database_module.models.app_model import AppModel


class Token(AppModel):
    """
    Class that define a token
    """

    # Foreign key field (user)
    user = fields.ForeignKeyField("models.User", related_name="tokens")
    token = fields.TextField()
    refresh_token = fields.TextField()

    class Meta:
        table = "token"

    @staticmethod
    def __name__() -> str:
        return "Token"

    def __str__(self) -> str:
        return f"{self.user}, {self.token}, {self.refresh_token}"
