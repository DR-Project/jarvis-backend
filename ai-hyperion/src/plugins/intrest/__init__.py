# import nonebot
from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


from nonebot.plugin import on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp import GroupMessageEvent

from . import data_source

import random

# Constant List

BOT_QNUM = ***
REG_QUESHI = '(确实|qs|有一说一|yysy)'
REG_DIUREN = '^(丢***|丢***|丢***|丢***|丢***|丢***|丢***|丢***|***)$'
REG_RDIUREN = '^(丢人|diuren|diu)$'


# Register Event

queshi = on_regex(REG_QUESHI)
random_diuren = on_regex(REG_RDIUREN)
diuren = on_regex(REG_DIUREN)


''' >>>>>> Just for fun <<<<<< '''


@queshi.handle()
async def _queshi(bot: Bot, event: MessageEvent):
    if(data_source.to_be_or_not_be(30)):
        text = '确实'
        await bot.send(event, text, at_sender=False)


@diuren.handle()
async def _diuren(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    if msg == "***":
        num = event.get_user_id()
        at_mem = [{
            'type': 'at',
            'data': {
                'qq': num
            }
        },{
            'type': 'text',
            'data': {
                'text': " 好逊哦，丢哪个胖 "
            }
        }]
    else:
        num = data_source.mem_dicts[msg]
        at_mem = [{
            'type': 'at',
            'data': {
                'qq': num
            }
        },{
            'type': 'text',
            'data': {
                'text': " 丢人 "
            }
        }]
    await bot.send(event, at_mem, at_sender=False)


@random_diuren.handle()
async def _random_diuren(bot: Bot, event: GroupMessageEvent):
    gid = event.group_id
    mem_list = await bot.get_group_member_list(group_id=gid, self_id=BOT_QNUM)
    lists = []
    for i in mem_list:
        lists.append(i['user_id'])
    lists.remove(BOT_QNUM)
    luck_dog = random.sample(lists, 1)[0]
    at_mem = [{
        'type': 'at',
        'data': {
            'qq': luck_dog
        }
    },{
        'type': 'text',
        'data': {
            'text': " 丢人 "
        }
    }]
    await bot.send(event, at_mem, at_sender=False)
