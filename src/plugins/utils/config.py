from pydantic import BaseSettings


class Config(BaseSettings):
    caiyun_apikey = '***'

    class Config:
        extra = "ignore"
