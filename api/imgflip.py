import requests
from collections import OrderedDict
import json
from urllib.parse import urlencode
from settings.settings import IMGFLIP_USER, IMGFLIP_PWD


def get_memes():
    get_memes_url = 'https://api.imgflip.com/get_memes'
    resp = requests.get(get_memes_url).json()
    if resp['success']:
        return resp


def craft_meme(id, text):
    caption_image_url = 'https://api.imgflip.com/caption_image'
    ln = len(text)
    i = 0
    data = {
        'template_id': id,
        'username': IMGFLIP_USER,
        'password': IMGFLIP_PWD,
        # 'text0': text0,
        # 'text1': text1,
    }
    while i < ln:
        data[f'boxes[{i}][text]'] = text[i]
        i += 1
    req = requests.post(caption_image_url, data=data).json()
    if req['success']:
        return req['data']['url']


def craft_meme_2(id):
    caption_image_url = 'https://api.imgflip.com/caption_image'
    data = {
        'template_id': id,
        'username': IMGFLIP_USER,
        'password': IMGFLIP_PWD,
        # 'text0': '0',
        # 'text1': '0',
        'boxes[0][text]': '1',
        'boxes[1][text]': '2',
        'boxes[2][text]': '',
        'boxes[3][text]': '4',

    }
    headers = {
        'Content-type': 'form-data'
    }
    req = requests.post(caption_image_url, data=data).json()
    # if req['success']:
    return req


if __name__ == '__main__':
    id = '93895088'
    r = get_memes()
    # r = craft_meme(id='14859329', text0='Просто текст', text1='Привет мир')

    boxes = [
        {'text': '1'},
        {'text': '2'},
        {'text': ''},
        {'text': '4'},
    ]

    # texts = ['1', '2', '3', '4']

    # boxes = (
    #     ('text', '1'),
    #     ('text', '2'),
    #     ('text', '3'),
    #     ('text', '4'),
    # )
    # r = craft_meme_2(id)
    print(r)
