import json
import httpx
import os, random
from typing import List

from .interface import lolicon


SWITCH_FLAG = False
PROT_B64 = 'base64://'
PROT_FILE = 'file:///'
DIR_MANAGER = '/src/data/'
DIR_CREEP_IMG = '/src/plugins/colorful/image/creep/'

async def get_colorful(lsp: int) -> str:
    msg = lolicon.get_lolicon()
    msg = msg['data'][0]
    url = str(msg['url'])
    pid = 'PID: ' + str(msg['pid']) + '\n'
    title = '标题: ' + msg['title'] + '\n'
    author = '作者: ' + msg['author'] + '\n'

    bitstream = lolicon.dump_img(url)
    b64_img = lolicon.convert_base64(bitstream)

    print(PROT_B64 + b64_img[:200])

    ret = [{
            'type': 'text',
            'data': {
                'text': pid
            }
        },{
            'type': 'text',
            'data': {
                'text': title
            }
        },{
            'type': 'text',
            'data': {
                'text': author
            }
        },{
            'type': 'image',
            'data': {
                'file': PROT_B64 + b64_img
            }
        },{
            'type': 'text',
            'data': {
                'text': '来啦来啦！'
            }
        },{
            'type': 'at',
            'data': {
                'qq': lsp
            }
        }]
    return ret


def get_crepper(lsp: int) -> str:
    ret = [{
            'type': 'image',
            'data': {
                'file': get_creep_path()
            }
        },{
            'type': 'text',
            'data': {
                'text': '不许色！'
            }
        },{
            'type': 'at',
            'data': {
                'qq': lsp
            }
        }]
    return ret


def get_file() -> str:
    file = os.getcwd() + DIR_MANAGER + 'manager.json'

    return file


def get_manager(file: str) -> List[str]:
    with open(file, mode='rb') as f:
        manager_object = f.read()
    
    manager_dict = json.loads(manager_object)
    owners = manager_dict['OWNER']
    admin = manager_dict['ADMIN']
    return owners +admin


def get_creep_path() -> str:
    img_dir = os.getcwd() + DIR_CREEP_IMG
    img_list = os.listdir(img_dir)
    luck_dog = random.sample(img_list, 1)[0]

    return PROT_FILE + img_dir + luck_dog


def premission_valid(user: str) -> bool:
    return user in get_manager(get_file())


if __name__ == '__main__':
    msg = get_colorful()['data'][0]
    print('PID: ' + str(msg['pid']))
