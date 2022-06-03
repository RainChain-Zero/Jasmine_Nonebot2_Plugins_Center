from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    reply_path =r"F:\Bot\NoneBot2\nonebot\src\plugins\nonebot_plugin_customizereply\customizedReply.json"
    favor_path =r"/home/mirai/Dice3349795206/UserConfDir/"
    favor_conf =r"/favorConf.json"
    class Config:
        extra = "ignore"