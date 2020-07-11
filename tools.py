import csv
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import PIL.Image as Image

file_path = "E:/OldChinese/Handian_Crawler/jia_jin_zhuan.csv"
root_dir = "E:/OldChinese/Handian_Crawler/data"
target_dir = "E:/OldChinese/Handian_Crawler/png_data"


def data_analysis():
    character_list = []
    with open(file_path, "r", encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        index = 0
        for line in reader:
            if index != 0:
                if 0 < int(line[2]) < 10:
                    character_list.append(line[4])
            index += 1
    return character_list


def get_all_list():
    character_list = []
    with open(file_path, "r", encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        index = 0
        for line in reader:
            if index != 0:
                character_list.append(line[4])
            index += 1
    return character_list


def svg2png(svg_file, png_file):
    drawing = svg2rlg(svg_file)
    renderPM.drawToFile(drawing, png_file, fmt="PNG")
    origin_image = Image.open(png_file)
    origin_image.resize((96, 96)).save(png_file, optimize=True)


def transfer_image_data():
    character_dir = os.scandir(root_dir)
    character_already_list = [target.name for target in os.scandir(target_dir)]
    for character in character_dir:
        if character.name not in character_already_list:
            target_character = target_dir + '/' + character.name
            print(target_character)
            if not os.path.exists(target_character):
                os.mkdir(target_character)
            type_dir = os.scandir(character)
            for character_type in type_dir:
                target_type = target_character + '/' + character_type.name
                if not os.path.exists(target_type):
                    os.mkdir(target_type)
                image_dir = os.scandir(character_type)
                for image in image_dir:
                    target_image = (target_type + '/' + image.name).replace('svg', 'png')
                    origin_image = (target_type + '/' + image.name).replace('png_data', 'data')
                    svg2png(origin_image, target_image)
            print('finish')


if __name__ == '__main__':
    transfer_image_data()
