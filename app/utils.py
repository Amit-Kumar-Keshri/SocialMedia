from passlib.context import CryptContext  # password hashing library

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto")  # password encrpyt


# for hashing password came from user
def hash(password: str):  # for hashing password came from user
    return pwd_context.hash(password)

def verify(plain_password, hashed_password): # for verifying password came from user & database
    return pwd_context.verify(plain_password, hashed_password)

