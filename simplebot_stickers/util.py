"""Module utilities"""

import functools
import random

import requests
from simplebot.bot import DeltaBot

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
)
session.request = functools.partial(session.request, timeout=15)  # type: ignore


def sizeof_fmt(num: float) -> str:
    suffix = "B"
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)  # noqa
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)  # noqa


def upload(bot: DeltaBot, path: str) -> str:
    urls = getdefault(bot, "cloud").split()
    random.shuffle(urls)
    for url in urls:
        try:
            with open(path, "rb") as file:
                with session.post(url, files=dict(file=file)) as resp:
                    if 200 <= resp.status_code <= 300:
                        return resp.text.strip()
        except Exception as ex:
            bot.logger.exception(ex)
    return ""


def getdefault(bot: DeltaBot, key: str, value: str = None) -> str:
    scope = __name__.split(".")[0]
    val = bot.get(key, scope=scope)
    if val is None and value is not None:
        bot.set(key, value, scope=scope)
        val = value
    return val
