from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    x_app_secret = '***'

    class Config:
        extra = "ignore"