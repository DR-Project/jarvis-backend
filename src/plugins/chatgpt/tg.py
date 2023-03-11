import json

import requests
from nonebot import get_driver, logger

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


def send_censored_msg(censored_msg: str, question: str) -> bool:
    url = 'https://api.telegram.org/bot%s/sendMessage' % config.tg_key

    data = {
        "chat_id": config.tg_chat_id,
        "text": '【ChatGPT】内容审查\n\n'
                + '问题：' + question + '\n\n'
                + '回答：' + censored_msg
    }

    r = requests.post(url, data=data)

    logger.info('暴力消息已被发送到TG机器人，内容是%s' % json.dumps(r.json()))

    if r.status_code == 200:
        return True
    return False
