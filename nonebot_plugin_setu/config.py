from pydantic import BaseSettings


class Config(BaseSettings):
    # 一次最大发送涩图量
    maxnum = 5
    # 用户数据文件夹
    conf_path = r"F:\Bot\mirai_console_diceplugin\Dice2632573315\user\UserConf"
    group_permission_path = r"/home/nonebot2/src/plugins/nonebot_plugin_setu/group_permission.json"
    # 管理员
    admin_list = [3032902237, 2677409596]
    # 合并转发涩图模式好感
    normal_favor_limit = 3000
    # 刷屏模式涩图好感
    boom_favor_limit = 3000
    # pivix PHPSESSID
    PHPSESSID = ''

    class Config:
        extra = "ignore"
