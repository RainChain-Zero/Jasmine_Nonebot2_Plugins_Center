from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    url = "http://localhost:45445/truth/"
    truth_pic_path = r"/home/nonebot2/data/truth/"

    class Config:
        extra = "ignore"
