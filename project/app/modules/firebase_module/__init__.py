from .firebase_manager import FirebaseManager

FirebaseModule = FirebaseManager()

__all__ = ["FirebaseModule", "register_firebase"]


def register_firebase() -> None:
    """
    Register the Firebase manager in the application
    """
    global FirebaseModule
    FirebaseModule.initialize()
