import secrets
import string

import bcrypt


def generate_random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def hash_password(raw_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(raw_password.encode(), salt).decode()
