from passlib.context import CryptContext  # password hashing library

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto")  # password encrpyt


def hash(password: str):
    return pwd_context.hash(password)

