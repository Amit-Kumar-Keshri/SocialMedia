from pydantic import BaseSettings


#environment variable validation
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #for config of database env variable access
    class Config:
        env_file = ".env"

settings = Settings()

# print(settings.database_username)
