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


from nonebot.plugin import on_regex, on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp import GroupMessageEvent

from . import data_source

import random

BOT_QNUM = ***

# Function for Utils 

queshi = on_regex('(确实|qs|有一说一|yysy)')
traffic = on_regex('^(查流量|魔法|Magic|magic)$')
cryptocoin = on_regex('^(BTC|btc|EOS|eos|BTG|btg|ADA|ada|DOGE|doge|LTC|ltc|ETH|eth)$')

@queshi.handle()
async def _queshi(bot: Bot, event: MessageEvent):
    text = '确实'
    await bot.send(event, text, at_sender=False)


@traffic.handle()
async def _traffic(bot: Bot, event: MessageEvent):
    dicts = data_source.magic_get_usage()
    result = data_source.magic_construct_string(dicts)
    await bot.send(event, result, at_sender=False)


@cryptocoin.handle()
async def _cryptocoin(bot: Bot, event: MessageEvent):
    coin_type = event.get_plaintext().upper()
    try:
        dicts = data_source.coin_get_price(data_source.cryptocurrency[coin_type])
        result = data_source.coin_construct_string(dicts)
    except: 
        result = "接口异常"
        await bot.send(event, result, at_sender=False)
    else:
        await bot.send(event, result, at_sender=False)


# Just for fun
diuren = on_regex('^(丢***|丢***|丢***|丢***|丢***|丢***)$')
@diuren.handle()
async def _diuren(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext()
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


random_diuren = on_regex('^(丢人|diuren|diu)$')
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


help_list = on_regex('^(Jarvis|贾维斯|命令列表)$')
@help_list.handle()
async def _help_list(bot: Bot, event: MessageEvent):
    lists = [{
        'type': 'text',
        'data': {
            'text': " __Command List v0.1__ \n"
        }
    },{
        'type': 'text',
        'data': {
            'text': " [Magic/魔法] \n> 查询Magic流量 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': " [BTG/LTC/...] \n> 数字货币价格 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': " [丢人/diu] \n> 随机抽取幸运儿 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': " [色来/selai] \n> 在鹿上了 0% \n",
        }
    }]
    await bot.send(event, lists, at_sender=False)