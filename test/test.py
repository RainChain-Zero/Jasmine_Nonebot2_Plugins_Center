from ruamel.yaml import YAML
import re
import requests

yml = YAML(typ='safe')

with open(r'src\plugins\test\Sea.yml', 'r', encoding='utf-8') as f:
    sea = yml.load(f)

with open('res.txt', 'a', encoding='utf-8') as f1:
    for bottle in sea['contents']:
        if bottle['type'] == 'BODY':
            continue
        owner = bottle['owner']
        qq = owner['id']
        nick = owner['name']
        groupObj = bottle['source']
        group = groupObj['id'] if groupObj else None
        groupName = groupObj['name'] if groupObj else None
        timeStamp = bottle['timestamp']

        content = bottle['content']
        content_li = content.split('}]}')
        content = content_li[0] if len(content_li) == 1 else content_li[1]
        if not 'PlainText' in content:
            continue
        content = content.split('},')
        content_res = []
        for c in content:
            res = re.findall(
                '{"type":"Image","imageId":"(.*)"', c)
            if res:
                content_res.append('[['+res[0]+']]')
            res = re.findall(
                '{"type":"PlainText","content":"(.*)"', c)
            if res:
                content_res.append(res[0])
        content = '\n'.join(content_res)
        if ('尸体' in content or '浮尸' in content):
            continue

        def is_chinese(string):
            """
            检查整个字符串是否包含中文
            :param string: 需要检查的字符串
            :return: bool
            """
            for ch in string:
                if u'\u4e00' <= ch <= u'\u9fff':
                    return True
            return False
        # 去除纯英文
        if (not is_chinese(content) and r'[[' not in content) or len(content) <= 6:
            continue
        res = requests.post('http://localhost:45445/bottle/throw', json={
            'type': 1, 'qq': qq, 'nick': nick, 'group': group, 'groupName': groupName, 'timeStamp': timeStamp, 'content': content}).json()
        if res['succ']:
            print('success')
        else:
            print('fail')
