import os

TORTOISE_ORM = {
    "connections": {
        # Predeterminated connection
        "default": os.environ.get("DATABASE_URL"),
        # Test database just in case we need it
        "test": os.environ.get("DATABASE_URL"),
    },
    "apps": {
        "models": {
            # route to models
            "models": ["app.modules.database_module.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
