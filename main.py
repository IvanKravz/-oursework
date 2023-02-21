import json
import requests
from pprint import pprint
from tqdm import tqdm
from time import sleep

class GetPhoto_VK:

    def __init__(self, token, vk_user_id, count):
        self.token = token
        self.vk_user_id = vk_user_id
        self.count = count
        self.json_list = []

    def request_get(self):
        api = requests.get('https://api.vk.com/method/photos.get', params = {
        'owner_id': self.vk_user_id,
        'access_token': self.token,
        'album_id': -6,
        'extended': 1,
        'count': self.count,
        'v': '5.131'
})
        # pprint(api.json()['response']['items'])
        return api.json()['response']['items']

    def photos(self):
        res = self.request_get()
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        list_photo = []
        for files in res:
            # Создаем словарь из имени (количество лайков_дата) и url
            name = {}
            name['file_name'] = f"{files['likes']['count']}_{files['date']}"
            size_max = max(files['sizes'], key=lambda x: vk_sizes[x['type']])
            name['url'] = size_max['url']
            # Создаем словарь для json
            name_json = {}
            name_json["file_name"] = f"{name['file_name']}" + '.jpg'
            name_json["size"] = size_max['type']
            list_photo.append(name)
            self.json_list.append(name_json)
        return list_photo

    def open_json(self, name):
        with open(name, "w") as f:
            json.dump(self.json_list, f, ensure_ascii=False, indent=2)

class YandexDisk:

    def __init__(self, token):
        self.token = token


    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload_file_to_disk(self, disk_file_path, list_photo):
        headers = self.get_headers()
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for photo_data in tqdm(list_photo):
            sleep(0.05)
            path = f"{disk_file_path}/{photo_data['file_name']}"
            url = photo_data['url']
            params = {"path": path, 'url': url, 'disable_redirects': True}
            requests.post(upload_url, headers=headers, params=params)
        print('Фотографии загружены')
            # if response.status_code == 202:
            #     print(f"Фотография {photo_data['file_name']} загружена")
            # else:
            #     print('Ошибка загрузки')

if __name__ == '__main__':
    vk = GetPhoto_VK(token="", vk_user_id='42203928', count=5)
    list_photo = vk.photos()
    ya = YandexDisk(token="")
    ya.upload_file_to_disk(disk_file_path="Netology", list_photo=list_photo)
    vk.open_json("new.json")

