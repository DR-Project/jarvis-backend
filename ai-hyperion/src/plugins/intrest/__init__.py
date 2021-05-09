from .config import Config

from nonebot import get_driver
from nonebot.plugin import on_regex
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

import random

from . import data_source

global_config = get_driver().config
config = Config(**global_config.dict())

# Constant List

BOT_QNUM = ***
REG_QUESHI = '(确实|qs|有一说一|yysy)'
REG_DIUREN = '^(丢***|丢***|丢***|丢***|丢***|丢***|丢***|丢***|***)$'
REG_RDIUREN = '^(丢人|diuren|diu)$'
REG_PLUS1S = '.*(蛤|蛤蛤|黑框眼镜).*'

# Register Event

queshi = on_regex(REG_QUESHI)
random_diuren = on_regex(REG_RDIUREN)
diuren = on_regex(REG_DIUREN)
plus1s = on_regex(REG_PLUS1S)

''' >>>>>> Just for fun <<<<<< '''


@queshi.handle()
async def _queshi(bot: Bot, event: MessageEvent):
    if (data_source.to_be_or_not_be(30)):
        text = '确实'
        await bot.send(event, text, at_sender=False)


@diuren.handle()
async def _diuren(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    if msg == "***":
        num = event.message_id
        at_mem = [{  # 新加的这个作为测试，没问题的话，就扩展到全部的食用性功能上面
            'type': 'reply',  # 这里改了一下，更符合逻辑。记得测试,
            # 如果不行，可能要在原来的基础上，加上这个，就是又要at type 又要reply type
            'data': {
                'id': num
            }
        }, {
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
        }, {
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
    }, {
        'type': 'text',
        'data': {
            'text': " 丢人 "
        }
    }]
    await bot.send(event, at_mem, at_sender=False)


@plus1s.handle()
async def plus1s(bot: Bot, event: MessageEvent):
    msg = "+1s"
    await bot.send(event, msg, at_sender=False)
