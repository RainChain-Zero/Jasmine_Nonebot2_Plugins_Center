from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    maxnum = 4
    saucenao_api_key="1fb776be717484116841cf67d84281e6c9877144"
    class Config:
        extra = "ignore"