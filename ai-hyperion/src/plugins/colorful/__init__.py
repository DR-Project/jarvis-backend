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

import os, random

# Constant List

DIR_IMAGE = '/src/plugins/colorful/image/creep/'
PROT_FILE = 'file:///'
REG_COLORFUL = '^(色来|色图|涩图|来点涩图|来点色图)$'

# Register Event

colorful = on_regex(REG_COLORFUL)


''' >>>>>> Core Function for Colorful <<<<<< '''


@colorful.handle()
async def _colorful(bot: Bot, event: MessageEvent):
    switch_flag = False
    if switch_flag:

        dicts = data_source.get_colorful()['data'][0]

        # init variable
        url = dicts['url']
        pid = 'PID: ' + str(dicts['pid']) + '\n'
        title = '标题: ' + dicts['title'] + '\n'
        author = '作者: ' + dicts['author'] + '\n'

        result = [{
            'type': 'text',
            'data': {
                'text': pid
            }
        }, {
            'type': 'text',
            'data': {
                'text': title
            }
        }, {
            'type': 'text',
            'data': {
                'text': author
            }
        }, {
            'type': 'image',
            'data': {
                'file': url
            }
        }]
    else:

        # get a random image from data warehouse
        img_dir = os.getcwd() + DIR_IMAGE
        img_list = os.listdir(img_dir)
        luck_dog = random.sample(img_list, 1)[0]
        img_path = PROT_FILE + img_dir + luck_dog
        lsp = event.get_user_id()

        result = [{
            'type': 'image',
            'data': {
                'file': img_path
            }
        }, {
            'type': 'text',
            'data': {
                'text': '不许色！'
            }
        }, {
            'type': 'at',
            'data': {
                'qq': lsp
            }
        }]

    await bot.send(event, result, at_sender=False)
