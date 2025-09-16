import secrets
import string

from passlib.context import CryptContext

# Creating passlib context
pwd_context = CryptContext(
    schemes=["bcrypt", "sha256_crypt", "django_pbkdf2_sha256"],
    deprecated="auto",
)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_temporal_pwd(lenght=8):
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(lenght))

    return password
