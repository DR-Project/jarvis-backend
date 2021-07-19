from .config import Config

from nonebot import get_driver, require
from nonebot.plugin import on_regex, on_keyword
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

import random, re

from . import data_source

global_config = get_driver().config
config = Config(**global_config.dict())
scheduler = require('nonebot_plugin_apscheduler').scheduler

# Constant List

BOT_QNUM = ***
REG_QUESHI = '(确实|qs|有一说一|yysy)'
REG_DIUREN = '***'
REG_RDIUREN = '^(丢人|diuren|diu)$'
REG_PLUS1S = '.*(蛤|蛤蛤|黑框眼镜).*'
REG_***_REPORT = '^(***排行|***ph|kk***)$'
REG_***_INDEX = '.*'
REG_POT = '***'
MC_DIU = '^(丢羊毛|有羊毛了|丢m记)$'

# Register Event

queshi = on_regex(REG_QUESHI)
random_diuren = on_regex(REG_RDIUREN)
diuren = on_regex(REG_DIUREN, re.IGNORECASE)
plus1s = on_regex(REG_PLUS1S)
***_index = on_regex(REG_***_INDEX)
***_report = on_regex(REG_***_REPORT, re.IGNORECASE)
diuren_pot = on_regex(REG_POT)
mc_diu = on_regex(MC_DIU, re.IGNORECASE)

''' >>>>>> Just for fun <<<<<< '''


@queshi.handle()
async def _queshi(bot: Bot, event: MessageEvent):
    if (data_source.to_be_or_not_be(30)):
        text = '确实'
        await bot.send(event, text, at_sender=False)


@diuren.handle()
async def _diuren(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
    if msg == '***':
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
                'text': ' 好逊哦，丢哪个胖 '
            }
        }]
    elif msg == '***':
        at_mem = [{
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }, {
            'type': 'text',
            'data': {
                'text': ' 丢人'
            }
        }]
    else:
        num = data_source.mem_dicts[msg[1:]]
        at_mem = [{
            'type': 'at',
            'data': {
                'qq': num
            }
        }, {
            'type': 'text',
            'data': {
                'text': ' 丢人 '
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
            'text': ' 丢人 '
        }
    }]
    await bot.send(event, at_mem, at_sender=False)

'''
@***_index.handle()
async def ***_index(bot: Bot, event: GroupMessageEvent):
    ret = str(event.get_message())
    ***_man = event.get_user_id()
    if ret.find('7f7177d2d24a93f532bac50ccfd02f70') != -1:
        ***_mans = await bot.get_group_member_info(group_id=event.group_id, user_id=***_man)
        ***_man_nick = ***_mans['card']
        await data_source.set_***_to_dict(***_man, ***_man_nick)
        msg = [{
            'type': 'reply',
            'data': {
                'id': event.message_id
            }
        }, {
            'type': 'text',
            'data': {
                'text': '你的***-1 '
            }
        }, {
            'type': 'at',
            'data': {
                'qq': ***_man
            }
        }]
        await bot.send(event, msg, at_sender=True)
    else:
        pass
'''

@diuren_pot.handle()
async def diuren_pot(bot: Bot, event: MessageEvent):
    at_mem = [{
        'type': 'at',
        'data': {
            'qq': ***
        }
    }, {
        'type': 'text',
        'data': {
            'text': ' 出来挨打 '
        }
    }]
    await bot.send(event, at_mem, at_sender=False)


@mc_diu.handle()
async def mc_diu(bot: Bot, event: MessageEvent):
    if event.get_user_id() == str(data_source.mem_dicts['***']):
        msg = [{
            'type': 'text',
            'data': {
                'text': '出来恰金拱门！🍟\n'
            }
        }, {
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }, {
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }, {
            'type': 'at',
            'data': {
                'qq': data_source.mem_dicts['***']
            }
        }]
        await bot.send(event, msg, at_sender=False)
    else:
        ret = [{
            'type': 'text',
            'data': {
                'text': '不许丢！🍟🍟🍟 \n'
            }
        }, {
            'type': 'at',
            'data': {
                'qq': event.get_user_id()
            }
        }]
        await bot.send(event, ret, at_sender=False)


@***_report.handle()
async def ***_report(bot: Bot, event: MessageEvent):
    msg = data_source.get_***_report()
    await bot.send(event, msg, at_sender=False)


@plus1s.handle()
async def plus1s(bot: Bot, event: MessageEvent):
    msg = '+1s'
    await bot.send(event, msg, at_sender=False)


async def ***_clear():
    data_source.mem_***s = {}


scheduler.add_job(***_clear, "cron", hour=0, id="***s")
