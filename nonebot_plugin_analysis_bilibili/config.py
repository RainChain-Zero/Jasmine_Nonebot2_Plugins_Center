from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    #! 不解析以下群
    group_ignore = [660991956]
    class Config:
        extra = "ignore"