from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    url = "http://localhost:45445/truth/"

    class Config:
        extra = "ignore"
