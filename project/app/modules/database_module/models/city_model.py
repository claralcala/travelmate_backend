from tortoise import fields

from app.modules.database_module.models.app_model import AppModel


class City(AppModel):
    """
    Class that define a city
    """

    name = fields.CharField(max_length=255, null=False)
    country = fields.CharField(max_length=255, null=False)

    class Meta:
        table = "city"

    @staticmethod
    def __name__() -> str:
        return "City"

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"
