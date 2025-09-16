from tortoise import fields

from app.modules.database_module.models.app_model import AppModel


class Trip(AppModel):
    """
    Class that define a trip
    """

    photo = fields.CharField(max_length=255, null=True)
    origin = fields.ForeignKeyField("models.City", related_name="origin_city")
    destination = fields.ForeignKeyField(
        "models.City", related_name="destination_city"
    )  # noqa: E501
    start_date = fields.DateField(null=False)
    end_date = fields.DateField(null=False)
    description = fields.TextField(null=True)
    day_count = fields.IntField(null=True)

    # Foreign key field (user)
    user = fields.ForeignKeyField("models.User", related_name="trips")
    # Foreign key field (transportation methods ) -many to many
    transportation_methods = fields.ManyToManyField(
        "models.TransportationMethod",
        related_name="trips",
        through="trip_transportation_method",
    )

    participants = fields.ManyToManyField(
        "models.User",
        related_name="trip_participants",
        through="trip_participant",
        null=True,
    )

    @staticmethod
    def __name__() -> str:
        return "Trip"

    def __str__(self) -> str:
        return (
            f"{self.origin}, {self.destination}, "
            f"{self.start_date}, {self.end_date}, "
            f"{self.description}"
        )
