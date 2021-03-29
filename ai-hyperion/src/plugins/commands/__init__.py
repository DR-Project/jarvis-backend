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

# Constant List

REG_HELP = '^(Jarvis|贾维斯|命令列表)$'
REG_IN_HELP = '^(里世界|整丶活)$'

# Register Event

help_list = on_regex(REG_HELP)
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
        'text': " 命令列表 -> 列出命令 \n",
    }
}

'''

@help_list.handle()
async def _help_list(bot: Bot, event: MessageEvent):
    lists = [{
        'type': 'text',
        'data': {
            'text': "✨ 目前可用 API ✨ \n"
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 CXLL -> 查询魔法流量 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 COIN -> 数字货币价格 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 药闻 -> 火星警察出动 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 命令列表 -> 列出命令 \n",
        }
    }]
    await bot.send(event, lists, at_sender=False)


@help_inlist.handle()
async def _help_inlist(bot: Bot, event: MessageEvent):
    lists = [{
        'type': 'text',
        'data': {
            'text': "✨ 里世界 API ✨ \n"
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 丢人 -> 随机抽取幸运儿 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 丢X -> 唯一指定丢人 \n",
        }
    },{
        'type': 'text',
        'data': {
            'text': "🍭 色来 -> 随机涩图抽卡 \n",
        }
    }]
    await bot.send(event, lists, at_sender=False)
