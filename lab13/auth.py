from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def validate_username(username):
    if len(username) < 3:
        return False, "Username must have at least 3 characters."

    if not re.fullmatch(r"[a-zA-Z0-9_]+", username):
        return False, "Use only letters, numbers and underscores."

    return True, ""


def validate_email(email):
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Enter a valid email address."

    return True, ""


def validate_password(password):
    if len(password) < 6:
        return False, "Password must have at least 6 characters."

    if not any(c.isdigit() for c in password):
        return False, "Password must contain a number."

    if not any(c.isalpha() for c in password):
        return False, "Password must contain a letter."

    return True, ""