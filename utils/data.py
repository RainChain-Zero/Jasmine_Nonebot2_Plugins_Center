import re
import requests


def read_favor(qq: int) -> int:
    try:
        resp = requests.get(
            f"http://localhost:45445/getFavor/{qq}", headers={'content-type': "application/json"}).json()
        return resp['data']
    except:
        return 0
