from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    favor_path ="F:\\Bot\\mirai_console_diceplugin\\Dice2632573315\\user\\UserConf\\"
    favor_conf ="\\favorConf.json"
    class Config:
        extra = "ignore"