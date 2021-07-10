import json
import httpx
import os, random
from typing import List

from .interface import lolicon

from src.data.manager import manager

SWITCH_FLAG = False
PROT_B64 = 'base64://'
PROT_FILE = 'file:///'
DIR_MANAGER = '/src/data/'
DIR_CREEP_IMG = '/src/plugins/colorful/image/creep/'


async def get_colorful(lsp: int) -> str:
    msg = lolicon.get_lolicon()[0]
    url = msg['url']
    pid = 'PID: ' + str(msg['pid']) + '\n'
    title = '标题: ' + msg['title'] + '\n'
    author = '作者: ' + msg['author'] + '\n'

    bitstream = lolicon.dump_img(url)
    try:
        bit_thread = lolicon.Base64Convertor(bitstream)
        bit_thread.start()
        bit_thread.join()
    except lolicon.ImageReadTimeout:
        return 'TIMEOUT'
    except lolicon.ImageRequestError:
        return '接口异常'

    b64_img = bit_thread.base64_str

    ret = [{
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
            'file': PROT_B64 + b64_img
        }
    }, {
        'type': 'text',
        'data': {
            'text': '来啦来啦！'
        }
    }, {
        'type': 'at',
        'data': {
            'qq': lsp
        }
    }]
    return ret


def get_creeper(lsp: int) -> str:
    ret = [{
        'type': 'image',
        'data': {
            'file': get_creep_path()
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
    return ret


def get_creep_path() -> str:
    img_dir = os.getcwd() + DIR_CREEP_IMG
    img_list = os.listdir(img_dir)
    luck_dog = random.sample(img_list, 1)[0]

    return PROT_FILE + img_dir + luck_dog


def permission_valid(user: str) -> bool:
    owner = manager['OWNER']
    admin = manager['ADMIN']
    managers = owner + admin
    return user in managers


'''if __name__ == '__main__':
    msg = get_colorful()['data'][0]
    print('PID: ' + str(msg['pid']))'''
