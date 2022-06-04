from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    max_num = 10

    class Config:
        extra = "ignore"
