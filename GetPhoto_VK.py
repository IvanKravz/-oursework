import requests
import json
from tqdm import tqdm
from YaUploader import YaUploader

class GetPhoto_VK:
    def __init__(self):
        self.token = input('Введите токен VK: ')
        self.vk_user_id = input('Введите ID пользователя VK: ')
        self.count = input('Введите количество фото: ')
        self.id_albom = input('Введите id альбома: ')
        self.ya = YaUploader()
        self.json_list = []
    def request_get(self):
        api = requests.get('https://api.vk.com/method/photos.get', params = {
        'owner_id': self.vk_user_id,
        'access_token': self.token,
        'album_id': self.id_albom,
        'extended': 1,
        'count': self.count,
        'v': '5.131'
})
        if api.status_code != 200:
            print('Отсутствует связь с сервером.')
        else:
            return api.json()['response']['items']
    def photos(self):
        res = self.request_get()
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        for files in tqdm(res):
            name = {}                                                    # Создаем словарь из имени (количество лайков_дата) и url
            name['file_name'] = f"{files['likes']['count']}_{files['date']}"
            size_max = max(files['sizes'], key=lambda x: vk_sizes[x['type']])   # определяем max значения из files['sizes']
            name['url'] = size_max['url']
            self.ya.get_foto(name['file_name'], name['url'])     # передаем в фун ya.get_foto значения 'file_name' и 'url' из словаря name
            self.json_list.append({"file_name": name['file_name'] + '.jpg', "size": size_max['type']})
        self.open_json()
    def open_json(self):                                             # Создаем файл foto.json и записываем в него self.json_list
        with open('foto.json', "w") as f:
            json.dump(self.json_list, f, ensure_ascii=False, indent=2)
