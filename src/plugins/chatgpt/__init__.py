import asyncio
import json
import re

import httpx
import nonebot
from nonebot import get_driver, on_message, logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Event, Message, GroupMessageEvent, MessageSegment
from nonebot.internal.rule import Rule
from nonebot.rule import to_me
from nonebot.typing import T_State

from .censor import AliyunCensor
from .config import Config
from .tg import send_censored_msg
from ..intrest.data_source import to_be_or_not_be

global_config = get_driver().config
config = Config(**global_config.dict())

chatgpt = on_message(rule=to_me())

HEADERS = {
    'x-app-secret': config.x_app_secret
}


def auto_reply_condition_checker():
    async def _checker(bot: Bot, event: GroupMessageEvent, state: T_State) -> bool:
        if not event.is_tome() and len(event.get_plaintext()) >= 7:
            if to_be_or_not_be(1):  # Numbers in brackets are hit probabilities
                state['addition'] = '\n请在20个字以内回复我'
                logger.info('[ChatGPT] 自动回复概率 命中')
                return True
            logger.info('[ChatGPT] 自动回复概率 没有命中')
            return False

    return Rule(_checker)


auto_reply = on_message(rule=auto_reply_condition_checker())


@auto_reply.handle()
@chatgpt.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    message = str(event.message)
    group_id = event.group_id

    if not message:
        logger.warning('空消息，正在结束该事件...')
        await chatgpt.finish()

    params = {
        'gid': group_id,
        'content': message + state.get('addition', '')
    }

    send_url = '***'

    r = httpx.get(url=send_url, params=params, headers=HEADERS)

    if r.json().get('code') != 0:
        await chatgpt.finish('出现未知错误')
    logger.info('消息[%s]发送成功' % message)

    mid = r.json().get('data').get('mid')
    logger.info('收到mid[mid=%s]' % mid)

    for i in range(10):
        logger.info('等待异步返回回复，第[%d]次轮询' % i)
        await asyncio.sleep(3)

        get_url = '***'

        params = {
            'gid': group_id,
            'mid': mid
        }

        r = httpx.get(get_url, params=params, headers=HEADERS)

        if r.json().get('code') != 0:
            await chatgpt.finish('出现未知错误')

        data = r.json().get('data')

        if data:
            message: str = [x.get('content') for x in data if x.get('role') == 'assistant'][0]
            msg = message.strip()
            logger.info('消息获取成功，消息是[%s]' % message)

            regex_chatgpt = re.compile('chatgpt', re.IGNORECASE)
            censor_msg = regex_chatgpt.sub(' 茶特寄屁替 ', msg, 999)

            regex_openai = re.compile('openai', re.IGNORECASE)
            censor_msg = regex_openai.sub(' O泡AI ', censor_msg, 999)

            regex_gpt = re.compile('gpt', re.IGNORECASE)
            censor_msg = regex_gpt.sub(' 寄屁替 ', censor_msg, 999)

            if AliyunCensor.is_block(censor_msg):
                send_censored_msg(censor_msg, message)
                await chatgpt.finish('内容太过暴力，请先完成相关备案')

            logger.info('发送审查后消息，消息是[%s]' % censor_msg)
            await chatgpt.finish(Message([MessageSegment.reply(event.message_id), censor_msg]))

    await chatgpt.finish('加载超时')




