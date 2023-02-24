import os
import httpx
import json, base64
from typing import List
from threading import Thread
from PIL import Image
from io import BytesIO


class Base64Convertor(Thread):
    base64_str = ''

    def __init__(self, image_base64):
        Thread.__init__(self)
        self.image_base64 = image_base64

    def run(self):
        self.base64_str = convert_base64(self.image_base64)


class ImageReadTimeout(Exception):
    pass


class ImageRequestError(Exception):
    pass


def get_lolicon() -> dict:
    """

    :return: msg is a dict from upstream method
    """
    url = 'https://api.lolicon.app/setu/'

    param = {
        'apikey': '***',
        'r18': '0'
    }

    # proxies = {
    #     'http://': 'http://localhost:7890',
    #     'https://': 'http://localhost:7890'
    # }

    try:
        r = httpx.get(url, params=param, timeout=45)

    except httpx.RequestError:

        raise Exception('Interface Error / 接口异常')

    else:

        payload = r.json()

    msg = payload['data']

    return msg


def dump_img(url: str) -> bytes:
    # proxies = {
    #     'http://': 'http://localhost:7890',
    #     'https://': 'http://localhost:7890'
    # }

    try:
        r = httpx.get(url)
    except httpx.RequestError:
        raise ImageRequestError('接口异常')
    except httpx.ReadTimeout:
        raise ImageReadTimeout('超时')
    else:
        image = r.content

    return image


def convert_base64(image: bytes) -> str:
    base64_str = str(base64.b64encode(image).decode('UTF-8'))

    return base64_str


if __name__ == '__main__':
    msg = get_lolicon()

    image = dump_img(msg[0]['url'])
    # print(convert_base64(image))

    try:
        t1 = Base64Convertor(image)
        t1.start()
        t1.join()
    except:
        print('66666')
    else:
        print(t1.base64_str)
        del t1
