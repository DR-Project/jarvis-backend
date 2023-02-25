from .config import Config

from nonebot import get_driver
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message

import re

global_config = get_driver().config
config = Config(**global_config.dict())

# Constant List

REG_HELP = '^(Jarvis|贾维斯|星期五|Friday|指令列表)$'
REG_EXP_HELP = '^(Hyperion)$'
REG_IN_HELP = '^(Alphas)$'

# Register Event

help_list = on_regex(REG_HELP, re.IGNORECASE)
help_explist = on_regex(REG_EXP_HELP)
help_inlist = on_regex(REG_IN_HELP)

''' >>>>>> Core Function for Commands <<<<<< '''

'''
命令列表 格式

✨ 目前可用 API ✨
🍭 CXLL -> 查询魔法流量
🍭 COIN -> 数字货币价格
🍭 丢人 -> 随机抽取幸运儿
🍭 丢X -> 唯一指定丢人
🍭 色来 -> 随机涩图抽卡
🍭 命令列表 -> 列出命令

{
    'type': 'text',
    'data': {
        'text': ' 命令列表 -> 列出命令 \n',
    }
}

'''


@help_list.handle()
async def _help_list(bot: Bot, event: MessageEvent):
    lists = Message()
    lists.append('✨ 目前可用 API ✨ \n')
    lists.append('🍭 CXLL -> 查询魔法流量 \n')
    lists.append('🍭 货币代号 -> 加密货币价格 \n')
    lists.append('🍭 热门货币 -> 热门货币市值 \n')
    lists.append('🍭 COVID -> 新冠疫情/疫苗报告 \n')
    lists.append('🍭 药闻 -> 火星警察出动 \n')
    lists.append('🍭 天气 -> 查询城市天气 \n')
    lists.append('🍭 DDL -> FedUni DDL \n')
    lists.append('🍭 丢人 -> 随机抽取幸运儿 \n')
    lists.append('🍭 丢X -> 唯一指定丢人 \n')
    lists.append('🍭 色来 -> 随机涩图抽卡 \n')
    lists.append('🍭 指令列表 -> 列出命令 \n')

    await help_list.finish(lists)


@help_explist.handle()
async def _help_explist(bot: Bot, event: MessageEvent):
    lists = Message()
    lists.append('✨ More API ✨ \n')
    lists.append('🍭 /ECOIN 币-对 -> 指定币对价格 \n')

    await help_explist.finish(lists)


@help_inlist.handle()
async def _help_inlist(bot: Bot, event: MessageEvent):
    lists = Message()
    lists.append('✨ Console API ✨ \n')
    lists.append('🍭 GO-status -> Status GO-CQHTTP \n')
    lists.append('🍭 GO-reload -> Reload GO-CQHTTP \n')

    await help_inlist.finish(lists)
