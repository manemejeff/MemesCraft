import requests
from collections import OrderedDict
import json
from urllib.parse import urlencode
from settings.settings import IMGFLIP_USER, IMGFLIP_PWD

get_memes_url = 'https://api.imgflip.com/get_memes'
caption_image_url = 'https://api.imgflip.com/caption_image'


def get_memes():
    resp = requests.get(get_memes_url).json()
    print(resp)
    if resp['success']:
        return resp


def craft_meme(meme_id, text):
    ln = len(text)
    i = 0
    data = {
        'template_id': meme_id,
        'username': IMGFLIP_USER,
        'password': IMGFLIP_PWD,
    }
    while i < ln:
        data[f'boxes[{i}][text]'] = text[i]
        i += 1
    req = requests.post(caption_image_url, data=data).json()
    if req['success']:
        return req['data']['url']


def get_demo_meme(meme_id: str, box_count: str):
    data = {
        'template_id': meme_id,
        'username': IMGFLIP_USER,
        'password': IMGFLIP_PWD,
    }

    box_count = int(box_count)
    for i in range(box_count):
        data[f'boxes[{i}][text]'] = i + 1

    req = requests.post(caption_image_url, data=data).json()
    if req['success']:
        return req['data']['url']


if __name__ == '__main__':
    pass
