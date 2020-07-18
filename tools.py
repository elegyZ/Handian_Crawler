import csv
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import PIL.Image as Image
import matplotlib.pyplot as plt

file_path = "E:/OldChinese/Handian_Crawler/jia_jin_zhuan.csv"
root_dir = "E:/OldChinese/Handian_Crawler/data"
target_dir = "E:/OldChinese/Handian_Crawler/left_data"
dataset_dir = "E:/OldChinese/unpaired_combined"


def data_analysis():
    character_list = []
    with open(file_path, "r", encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        index = 0
        for line in reader:
            if index != 0 and int(line[2]) >= 10:
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
    # character_dir = os.scandir(root_dir)
    character_already_list = [target.name for target in os.scandir(target_dir)]
    for character in list_jia:
        source_type = root_dir + '/' + character + '/' + '金文'
        target_type = target_dir + '/' + character + '/' + '金文'
        if os.path.exists(source_type):
            print(source_type)
            if not os.path.exists(target_dir + '/' + character):
                os.mkdir(target_dir + '/' + character)
            os.mkdir(target_type)
            image_dir = os.scandir(source_type)
            for image in image_dir:
                target_image = (target_type + '/' + image.name).replace('svg', 'png')
                origin_image = (target_type + '/' + image.name).replace('left_data', 'data')
                print(origin_image)
                svg2png(origin_image, target_image)
            print('finish')
        # if character.name not in character_already_list:
        #     target_character = target_dir + '/' + character.name
        #     print(target_character)
        #     if not os.path.exists(target_character):
        #         os.mkdir(target_character)
        #     type_dir = os.scandir(character)
        #     for character_type in type_dir:
        #         target_type = target_character + '/' + character_type.name
        #         if not os.path.exists(target_type):
        #             os.mkdir(target_type)
        #         image_dir = os.scandir(character_type)
        #         for image in image_dir:
        #             target_image = (target_type + '/' + image.name).replace('svg', 'png')
        #             origin_image = (target_type + '/' + image.name).replace('png_data', 'data')
        #             svg2png(origin_image, target_image)
        #     print('finish')


def dataset_analysis():
    type_list = ['jia', 'jin', 'chu', 'qin', 'zhuan']
    type_dic = dict()
    for type_name in type_list:
        type_dir = dataset_dir + '/' + type_name
        character_list = os.listdir(type_dir)
        type_dic[type_name] = character_list
    for source_name in type_list:
        for mid_name in type_list:
            for target_name in type_list:
                for final_name in type_list:
                    result = list(set(type_dic[source_name]).intersection(set(type_dic[mid_name]))
                                  .intersection(set(type_dic[target_name])).intersection(set(type_dic[final_name])))
                    print(source_name, mid_name, target_name, final_name, len(result))


def line_graph():
    type_list = ['jia', 'jin', 'chu', 'qin', 'zhuan']
    type_image_list = []
    for type_name in type_list:
        type_dir = dataset_dir + '/' + type_name
        image_dic = dict()
        for character_dir in os.scandir(type_dir):
            image_num = int(len(os.listdir(character_dir)) / 10)
            if image_num not in image_dic:
                image_dic[image_num] = 1
            else:
                image_dic[image_num] += 1
        image_list = sorted(image_dic.items(), key=lambda d: d[0])
        key_list, item_list = [], []
        for pair in image_list:
            key_list.append(pair[0] * 10 + 10)
            item_list.append(pair[1])
        draw_line_graph(key_list, item_list)


def draw_line_graph(key_list, item_list):
    plt.bar(key_list, item_list, width=1)
    plt.xlabel('range of item number')
    plt.ylabel('the number of characters')
    plt.show()


if __name__ == '__main__':
    line_graph()
