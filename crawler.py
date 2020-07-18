import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import requests
import os
import re
import tools


def get_character_types(character, special_type=None):
    """
    This function is for getting the exist type list of a character.
    :param special_type: the special type which the crawler will only focus on
    :param character: a string of a character
    :return :
    """
    root_path = 'https://www.zdic.net/hans/'
    root_dir = "E:/OldChinese/Handian_Crawler/data/"
    character_dir = root_dir + character
    page_path = urllib.request.quote(root_path + character, safe=";/?:@&=+$,", encoding="utf-8")
    response = urllib.request.urlopen(page_path)
    if response.getcode() != 200:
        print('The HTML Page Can Not Open Correctly.')
    else:
        soup = BeautifulSoup(response.read(), 'html.parser')
        div = soup.find('div', class_='zylink')
        if div is not None:
            items = div.find_all('a')
            type_list = [(str(item.string), str(item.get('href'))) for item in items]
            get_character_images(character_dir, type_list, special_type)


def get_character_images(character_dir, type_list, special_type=None):
    """
    This function is for getting the image address for each type of in the type_list.
    And download the images for each address list.
    :param special_type: the special type which the crawler will only focus on
    :param character_dir: the local directory of a character's images
    :param type_list: a list of tuples, which contains the type and address of the character
    :return:
    """
    root_path = "https://www.zdic.net/"
    for character_type, address in type_list:
        type_dir = character_dir + '/' + character_type
        if special_type is not None:
            if character_type == special_type:
                if not os.path.exists(character_dir):
                    os.mkdir(character_dir)
                if not os.path.exists(type_dir):
                    os.mkdir(type_dir)
                print(character_dir)
                reach_images(root_path + address, type_dir)
                return
        else:
            if not os.path.exists(character_dir):
                os.mkdir(character_dir)
            if not os.path.exists(type_dir):
                os.mkdir(type_dir)
            print(character_dir)
            reach_images(root_path + address, type_dir)


def reach_images(url_path, type_dir):
    """
    The function will reach the page which contains the images of the character
    :param url_path: the HTML address
    :param type_dir: the local path for save images
    :return:
    """
    page_path = urllib.request.quote(url_path, safe=";/?:@&=+$,", encoding="utf-8")
    response = urllib.request.urlopen(page_path)
    if response.getcode() != 200:
        print('The HTML Page Can Not Open Correctly.')
    else:
        soup = BeautifulSoup(response.read(), 'html.parser')
        div_list = soup.find_all('div', class_='zy')
        address_list = [div.find('img').get('data-original') for div in div_list]
        download_images(type_dir, address_list, str(page_path))


def download_images(type_dir, address_list, referer_address):
    """
    The function will download the images of characters and save them on the local memory
    :param type_dir: the local directory for saving this type of images
    :param address_list: the address of the url page
    :param referer_address: the information in the header
    :return:
    """
    headers = {"Referer": referer_address,
               "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/83.0.4103.106 Safari/537.36"}
    for address in address_list:
        root_path = "https:"
        html = requests.get(root_path + address, headers=headers)
        image_name = re.search('\d.+', address).group()
        image_dir = type_dir + '/' + image_name
        with open(image_dir, 'wb') as file:
            file.write(html.content)
            file.flush()
        file.close()
    print(type_dir + "下载完成")


if __name__ == '__main__':
    root_dir = "E:/OldChinese/Handian_Crawler/data"
    character_list = tools.data_analysis()
    for index, char in enumerate(character_list[350:]):
        if index % 50 == 0:
            print(index)
        if not os.path.exists(root_dir + '/' + char + '/金文'):
            get_character_types(char, "金文")
