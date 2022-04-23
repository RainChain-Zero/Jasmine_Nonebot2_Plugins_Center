from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    reply_path =r"/home/nonebot2/src/plugins/nonebot_plugin_customizereply/customizedReply.json"
    class Config:
        extra = "ignore"