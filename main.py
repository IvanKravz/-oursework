from GetPhoto_VK import GetPhoto_VK
from YaUploader import YaUploader

if __name__ == '__main__':
    vk = GetPhoto_VK()
    ya = YaUploader()
    foto_list = vk.photos()
    ya.upload_file(foto_list)