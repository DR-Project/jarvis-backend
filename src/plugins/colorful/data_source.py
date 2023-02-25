import json
import os
import random

from typing import List, Union
from nonebot.adapters.onebot.v11 import MessageSegment, Message

from .interface import lolicon

SWITCH_FLAG = False
PROT_B64 = 'base64://'
PROT_FILE = 'file:///'
DIR_MANAGER = '/src/data/'
DIR_CREEP_IMG = '/src/plugins/colorful/image/creep/'


async def get_colorful(lsp: int) -> Union[Message, str]:
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

    return Message([pid, title, author, MessageSegment.image(PROT_B64 + b64_img), '来啦来啦！', MessageSegment.at(lsp)])


def get_crepper(lsp: int) -> Message:

    return Message([MessageSegment.image(get_creep_path()), '不许色！', MessageSegment.at(lsp)])


def get_file() -> str:
    file = os.getcwd() + DIR_MANAGER + 'manager.json'

    return file


def get_manager(file: str) -> List[str]:
    with open(file, mode='rb') as f:
        manager_object = f.read()

    manager_dict = json.loads(manager_object)
    owners = manager_dict['OWNER']
    admin = manager_dict['ADMIN']
    return owners + admin


def get_creep_path() -> str:
    img_dir = os.getcwd() + DIR_CREEP_IMG
    img_list = os.listdir(img_dir)
    luck_dog = random.sample(img_list, 1)[0]

    return PROT_FILE + img_dir + luck_dog


def permission_valid(user: Union[int, str]) -> bool:
    return user in get_manager(get_file())


'''if __name__ == '__main__':
    msg = get_colorful()['data'][0]
    print('PID: ' + str(msg['pid']))'''
