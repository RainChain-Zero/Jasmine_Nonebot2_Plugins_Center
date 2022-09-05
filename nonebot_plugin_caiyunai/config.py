from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    caiyunai_apikey: str = "62c2f1a9cf04bf13e9c512d6"
    proxies: str = "http://127.0.0.1:15777"
    favor_path ="F:\\Bot\\mirai_console_diceplugin\\Dice2632573315\\user\\UserConf\\"
    favor_conf ="\\favorConf.json"