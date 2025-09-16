from tortoise import fields

from app.modules.database_module.models.app_model import AppModel


class TransportationMethod(AppModel):

    name = fields.CharField(max_length=255, null=False)

    @staticmethod
    def __name__() -> str:
        return "TransportationMethod"

    def __str__(self) -> str:
        return f"{self.name}"
