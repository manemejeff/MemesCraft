import requests
from settings.settings import IMGFLIP_USER, IMGFLIP_PWD


def get_memes():
    get_memes_url = 'https://api.imgflip.com/get_memes'
    resp = requests.get(get_memes_url).json()
    if resp['success']:
        return resp
    else:
        raise Exception(message='Error during api request')


def craft_meme(id, text0, text1):
    caption_image_url = 'https://api.imgflip.com/caption_image'
    data = {
        'template_id': id,
        'username': IMGFLIP_USER,
        'password': IMGFLIP_PWD,
        'text0': text0,
        'text1': text1,
    }
    req = requests.post(caption_image_url, data=data).json()
    if req['success']:
        return req['data']['url']
    else:
        raise Exception(message='Error during image caption')

r = get_memes()
# r = craft_meme(id='14859329', text0='Просто текст', text1='Привет мир')

print(r)
