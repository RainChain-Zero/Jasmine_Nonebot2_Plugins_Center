from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    reply_path =r"F:\Bot\NoneBot2\nonebot\src\plugins\nonebot_plugin_customizereply\customizedReply.json"
    class Config:
        extra = "ignore"