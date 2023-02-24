
import requests
class YaUploader:
    def __init__(self):
        self.token = input('Введите токен YandexDisk: ')
        self.yandex_folder = input('Введите название яндекс-папки: ')
        self.new_folder()
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
    def new_folder(self):
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": self.yandex_folder, 'overwrite': 'true'}
        response = requests.put(url, headers=headers, params=params)
        if response.status_code != 201:
            print(f'Папка с именем: {self.yandex_folder} уже существует!')
        else:
            print(f'Папка: {self.yandex_folder} создана на Yandex disk')
    def upload_file_to_disk(self, file_path, url):
        headers = self.get_headers()
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": file_path, 'url': url, 'disable_redirects': True}
        response = requests.post(upload_url, headers=headers, params=params)
        if response.status_code == 202:
            print('Фотография загружена')
        else:
            print('Ошибка загрузки')

    def get_foto(self, file_name, url):
        file_path = self.yandex_folder + '/' + file_name
        self.upload_file_to_disk(file_path, url)