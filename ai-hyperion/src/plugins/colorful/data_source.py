import json
import httpx
import os, random
from typing import List

from .interface import lolicon

SWITCH_FLAG = False
PROT_FILE = 'file:///'
DIR_MANAGER = '/src/data/'
DIR_CREEP_IMG = '/src/plugins/colorful/image/creep/'

def get_colorful() -> str:
    ret = lolicon.construct_string(lolicon.get_lolicon())

    return ret


def get_crepper(lsp: int) -> str:
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


def get_file() -> str:
    file = os.getcwd() + DIR_MANAGER + 'manager.json'

    return file


def get_manager(file: str) -> List[str]:
    with open(file, mode='rb') as f:
        manager_object = f.read()
    
    manager_dict = json.loads(manager_object)
    owners = manager_dict['OWNER']
    
    return owners


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
