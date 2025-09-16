import os
from io import BytesIO

import firebase_admin
from firebase_admin import credentials, storage

from app.schemas.photo_schema import PhotoOutputSchema


class FirebaseManager:

    def __init__(self):
        self.bucket = None

    def initialize(self):
        credentials_path = os.path.join(
            os.path.dirname(__file__), "firebase_credentials.json"
        )  # noqa: E501

        cred = credentials.Certificate(credentials_path)

        firebase_admin.initialize_app(
            cred, {"storageBucket": "fct24-89e51.appspot.com"}
        )

        self.bucket = storage.bucket()

    def upload_photo(
        self, photo_io: BytesIO, file_name: str, user_id: int
    ) -> PhotoOutputSchema:

        blob = self.bucket.blob(f"profile_pictures/{user_id}/{file_name}")
        blob.upload_from_file(photo_io, content_type="image/jpeg")
        blob.make_public()
        photo_url = blob.public_url

        return PhotoOutputSchema(photo_url=photo_url)
