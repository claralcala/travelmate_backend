from tortoise import fields

from app.modules.database_module.models.app_model import AppModel
from app.modules.database_module.models.trip_model import Trip


class User(AppModel):
    """
    Class that define a user
    """

    nickname = fields.CharField(max_length=255, null=False)
    password = fields.CharField(max_length=255, null=False)
    photo = fields.CharField(max_length=500000, null=True)
    email = fields.CharField(max_length=255, null=False)
    birthdate = fields.DateField(null=False)
    name = fields.CharField(max_length=255, null=False)
    surname = fields.CharField(max_length=255, null=True)
    description = fields.CharField(max_length=2000, null=True)

    trips: fields.ReverseRelation["Trip"]

    @staticmethod
    def __name__() -> str:
        return "User"

    def __str__(self) -> str:
        return (
            f"{self.nickname}, {self.password}, {self.photo}, "
            f"{self.email}, {self.birthdate}, {self.name}, {self.surname}"
        )
