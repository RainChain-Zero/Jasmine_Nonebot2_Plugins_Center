from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    maxnum = 4
    google_baidu_maxnum = 10
    saucenao_api_key="1fb776be717484116841cf67d84281e6c9877144"
    ehentai_cookies = "ipb_session_id=7ee2c4370e36ce2f1ffc3026f1ced2ff; ipb_member_id=6595583; ipb_pass_hash=eb5ea7c375f5875bb5eaf43aa515f839; sk=d3pv9vz64es80agpp5rkwjouaxgi" 
    favor_path ="F:\\Bot\\mirai_console_diceplugin\\Dice2632573315\\user\\UserConf\\"
    favor_conf ="\\favorConf.json"
    cache_path = r"F:\Bot\NoneBot2\nonebot\data\picsearcher"
    class Config:
        extra = "ignore"