from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://postgres:Roksi2015@localhost:5432/web_13 "
    SECRET_KEY_JWT: str = "@43r4645ybgscsss4w"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "postgres@meail.com"
    MAIL_PASSWORD: str = "postgres"
    MAIL_FROM: str = "postgres"
    MAIL_PORT: int = 567234
    MAIL_SERVER: str = "postgres"
    REDIS_DOMAIN: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLD_NAME: str = 'dlraufrwg'
    CLD_API_KEY: int = 327154174922339 
    CLD_API_SECRET: str = "XONtM01vGvh7LGIZhSYxVkpYB7E "

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        """
        The validate_algorithm function is a validator that ensures the algorithm used to sign the JWT is either HS256 or HS512.
            This function will raise a ValueError if an invalid algorithm is passed in.
        
        :param cls: Pass the class that is being validated
        :param v: Any: Validate the value of the algorithm
        :return: A value
        :doc-author: Trelent
        """
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v


    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()