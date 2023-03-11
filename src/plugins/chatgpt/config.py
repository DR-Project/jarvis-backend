from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    x_app_secret = '***'
    tg_key = '***'
    tg_chat_id = '***'

    class Config:
        extra = "ignore"