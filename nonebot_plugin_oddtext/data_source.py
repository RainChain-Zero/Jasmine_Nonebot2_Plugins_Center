import math
import random

from dataclasses import dataclass
from typing import Tuple, Protocol

from .flip import flip_table
from .cxh import emoji, pinyin
from .bug import bug_code, bug_level
from .hxw import enchars, encharhxw, ftw, hxw, jtw


def cxh_text(text: str) -> str:
    def get_pinyin(s):
        if s in pinyin:
            return pinyin[s]
        return ""

    result = ""
    for i in range(len(text)):
        pinyin1 = get_pinyin(text[i])
        pinyin2 = get_pinyin(text[i + 1]) if i < len(text) - 1 else ""
        if pinyin1 + pinyin2 in emoji:
            result += emoji[pinyin1 + pinyin2]
        elif pinyin1 in emoji:
            result += emoji[pinyin1]
        else:
            result += text[i]
    return result


def hxw_text(text: str) -> str:
    result = ""
    for s in text:
        c = s
        if s in enchars:
            c = encharhxw[enchars.index(s)]
        elif s in jtw:
            c = hxw[jtw.index(s)]
        elif s in ftw:
            c = hxw[ftw.index(s)]
        result += c
    return result


def ant_text(text: str) -> str:
    result = ""
    for s in text:
        result += s + chr(1161)
    return result


def flip_text(text: str) -> str:
    text = text.lower()
    result = ""
    for s in text[::-1]:
        result += flip_table[s] if s in flip_table else s
    return result


def bug_text(text: str) -> str:
    def bug(p, n):
        result = ""
        if isinstance(n, list):
            n = math.floor(random.random() * (n[1] - n[0] + 1)) + n[0]
        for i in range(n):
            result += bug_code[p][int(random.random() * len(bug_code[p]))]
        return result

    level = 12
    u = bug_level[level]
    result = ""
    for s in text:
        result += s
        if s != " ":
            result += (
                bug("mid", u["mid"])
                + bug("above", u["above"])
                + bug("under", u["under"])
                + bug("up", u["up"])
                + bug("down", u["down"])
            )
    return result


class Func(Protocol):
    def __call__(self, text: str) -> str:
        ...


@dataclass
class Command:
    keywords: Tuple[str, ...]
    func: Func


commands = [
    Command(("抽象话",), cxh_text),
    Command(("火星文",), hxw_text),
    Command(("蚂蚁文",), ant_text),
    Command(("翻转文字",), flip_text),
    Command(("故障文字",), bug_text),
]
