import PIL.Image as img
from PIL import ImageFont, ImageDraw,Image
import os
import json
import random


def image_add_text(xmin_v,ymin_v,xmax_v,ymax_v,count,name_count,m):
    if count == 0:
        IMG = './picture/%d.jpg'%name_count
    else:
        IMG = './output/%d.jpg'%name_count
    text = m.encode("utf-8")
    im = img.open(IMG)
    x_long = im.size[0]

    size = x_long / 1440
    xmin = xmin_v * size
    ymin = ymin_v * size
    xmax = xmax_v * size

    x_rand = int((xmin - xmax) / 2)
    x_add = xmax - random.randint(x_rand, abs(x_rand))
    y_add = ymin

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("msyh.ttf", 40)
    draw.text([round(x_add), round(y_add)], m, fill = (169,169,169), font=font)
    im.save('output/%d.jpg'%name_count)

def image_add_image(xmin_v,ymin_v,xmax_v,ymax_v,count,name_count,m):
    if count == 0:
        IMG = './picture/%d.jpg'%name_count
    else:
        IMG = './output/%d.jpg'%name_count

    IMG2 = './IMG/1.jpg'
    im = img.open(IMG)
    im2 = img.open(IMG2)
    x_long = im.size[0]
    x_long_2 = im2.size[0]
    x_w_2 = im2.size[1]
    size = x_long / 1440
    xmin = xmin_v * size
    ymin = ymin_v * size
    xmax = xmax_v * size
    ymax = ymax_v * size
    x_rand = (xmin - xmax + x_long_2)/2
    y_rand = (ymin - ymax + x_w_2)/2
    x_add = xmin + abs(x_rand)
    y_add = ymin + abs(y_rand)
    x_rand_1 = abs(xmax - xmin)
    y_rand_1 = abs(ymax - ymin)

    image = Image.new(mode="RGB", size=(round(x_rand_1), round(y_rand_1)), color = (255,255,255))
    im.paste(image, (round(xmin), round(ymin)))
    im.paste(im2, (round(x_add), round(y_add)))
    im.save('output/%d.jpg'%name_count)

def image_add_null(xmin_v,ymin_v,xmax_v,ymax_v,count,name_count,m):
    if count == 0:
        IMG = './picture/%d.jpg'%name_count
    else:
        IMG = './output/%d.jpg'%name_count

    mm = []
    im = img.open(IMG)
    x_long = im.size[0]
    size = x_long / 1440
    xmin = xmin_v * size
    ymin = ymin_v * size
    xmax = xmax_v * size
    ymax = ymax_v * size
    aa = xmin
    bb = ymin
    x_rand_1 = round(abs(xmax - xmin))
    y_rand_1 = round(abs(ymax - ymin))
    mm.append(aa)
    mm.append(bb)
    cc = tuple(mm)
    c = im.getpixel(cc)
    image = Image.new(mode="RGB", size=(x_rand_1, y_rand_1), color = c)
    im.paste(image, (round(xmin), round(ymin)))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("msyh.ttf", 40)
    aaa = 'null'
    draw.text([xmin , ymin], aaa, fill = (169,169,169), font=font)
    im.save('output/%d.jpg'%name_count)
    mm =[]

def image_c_o(xmin_v,ymin_v,xmax_v,ymax_v,count,name_count,m):
    if count == 0:
        IMG = './picture/%d.jpg'%name_count
    else:
        IMG = './output/%d.jpg'%name_count

    mm = []
    im = img.open(IMG)
    x_long = im.size[0]
    size = x_long / 1440
    xmin = xmin_v * size
    ymin = ymin_v * size
    xmax = xmax_v * size
    ymax = ymax_v * size
    aa = xmin
    bb = ymax
    rand = random.random()
    x_rand_1 = round(abs(xmax - xmin))
    y_rand_1 = round(abs(ymax - ymin) * rand * 0.4)
    mm.append(aa)
    mm.append(bb)
    cc = tuple(mm)
    c = im.getpixel(cc)

    image = Image.new(mode="RGB", size=(x_rand_1, y_rand_1), color = c)
    im.paste(image, (round(xmin), round(ymin + y_rand_1)))
    im.save('output/%d.jpg'%name_count)
    mm =[]



def android_text(json_dict,name_count):
    nodes = []
    root = json_dict['activity']['root']
    nodes.append(root)
    idx_pointer = 0

    while len(nodes) > idx_pointer:
        node = nodes[idx_pointer]
        if 'children' in node:
            nodes.extend((node.pop('children')))
        idx_pointer += 1

    a = {}
    b = {}
    m = ''
    count = 0
    IMG = './picture/%d.jpg' % name_count
    im = img.open(IMG)
    x_long = im.size[0]

    for i in range(len(nodes)):
        a = nodes[i]
        for k, v in a.items():
            if k == 'text':
                if v != '':
                    b = a
                    m = v
        for k1, v1 in b.items():
            if k1 == 'bounds':
                rand_num = random.randint(0,10)
                if rand_num <= 6:
                    x_min_v = v1[0]
                    y_min_v = v1[1]
                    x_max_v = v1[2]
                    y_max_v = v1[3]
                    ymin = y_min_v * 0.75

                    if ymin >= 320 and ymin <= 1600 and x_long == 1080:
                        image_add_text(x_min_v, y_min_v, x_max_v, y_max_v, count, name_count, m)
                        count += 1

        b = {}
        a = {}


def android_null(json_dict,name_count):
    nodes = []
    root = json_dict['activity']['root']
    nodes.append(root)
    idx_pointer = 0

    while len(nodes) > idx_pointer:
        node = nodes[idx_pointer]
        if 'children' in node:
            nodes.extend((node.pop('children')))
        idx_pointer += 1

    a = {}
    b = {}
    m = ''
    count = 0
    IMG = './picture/%d.jpg' % name_count
    im = img.open(IMG)
    x_long = im.size[0]

    for i in range(len(nodes)):
        a = nodes[i]
        for k, v in a.items():
            if k == 'text':
                if v != '':
                    b = a
                    m = v
        for k1, v1 in b.items():
            if k1 == 'bounds':
                rand_num = random.randint(0,10)
                if rand_num <= 4:

                    x_min_v = v1[0]
                    y_min_v = v1[1]
                    x_max_v = v1[2]
                    y_max_v = v1[3]
                    xmin = x_min_v * 0.75
                    ymin = y_min_v * 0.75

                    if ymin >= 320 and ymin <= 800 and x_long == 1080:
                        if xmin >=20 and xmin < 500:
                            image_add_null(x_min_v, y_min_v, x_max_v, y_max_v, count, name_count, m)
                            count += 1

        b = {}
        a = {}


def android_image(json_dict,name_count):
    nodes = []
    root = json_dict['activity']['root']
    nodes.append(root)
    idx_pointer = 0

    while len(nodes) > idx_pointer:
        node = nodes[idx_pointer]
        if 'children' in node:
            nodes.extend((node.pop('children')))
        idx_pointer += 1

    a = {}
    b = {}
    count = 0
    IMG = './picture/%d.jpg' % name_count
    im = img.open(IMG)
    x_long = im.size[0]
    for i in range(len(nodes)):
        a = nodes[i]
        for k, v in a.items():
            s = str(v)
            m = s.find('ImageView')
            if m > 0:
                b = a
        for k1, v1 in b.items():
            if k1 == 'bounds':
                rand_num = random.randint(0,10)
                if rand_num <= 4:

                    x_min_v = v1[0]
                    y_min_v = v1[1]
                    x_max_v = v1[2]
                    y_max_v = v1[3]

                    xmin = x_min_v * 0.75
                    ymin = y_min_v * 0.75
                    xmax = x_max_v * 0.75
                    ymax = y_max_v * 0.75
                    x_rand_1 = int((xmax - xmin))
                    y_rand_1 = int((ymax - ymin))
                    if ymin >= 320 and ymin <= 1600 and x_rand_1>1 and x_long == 1080:
                            image_add_image(x_min_v, y_min_v, x_max_v, y_max_v, count, name_count, m)
                            count += 1

        b = {}
        a = {}

def android_c_o(json_dict,name_count):
    nodes = []
    root = json_dict['activity']['root']
    nodes.append(root)
    idx_pointer = 0

    while len(nodes) > idx_pointer:
        node = nodes[idx_pointer]
        if 'children' in node:
            nodes.extend((node.pop('children')))
        idx_pointer += 1

    a = {}
    b = {}
    m = ''
    count = 0
    IMG = './picture/%d.jpg' % name_count
    im = img.open(IMG)
    x_long = im.size[0]

    for i in range(len(nodes)):
        a = nodes[i]
        for k, v in a.items():
            if k == 'text':
                if v != '':
                    b = a
                    m = v
        for k1, v1 in b.items():
            if k1 == 'bounds':
                rand_num = random.randint(0,10)
                if rand_num <= 4:

                    x_min_v = v1[0]
                    y_min_v = v1[1]
                    x_max_v = v1[2]
                    y_max_v = v1[3]

                    xmin = x_min_v * 0.75
                    ymin = y_min_v * 0.75

                    if ymin >= 320 and ymin <= 800 and x_long == 1080:
                        if xmin >=20 and xmin < 500:
                            image_c_o(x_min_v, y_min_v, x_max_v, y_max_v, count, name_count, m)
                            count += 1

        b = {}
        a = {}


if __name__ == "__main__":
    name_count = 0
    file_path = "json"
    path_list = os.listdir(file_path)
    path_name = []
    for i in path_list:
        path_name.append(int(i.split(".")[0]))
    path_name.sort()
    print(path_name)

    for file_name in path_name:
        name_count = int(file_name)
        if name_count > 1:
            with open('json/%d.json'%name_count, 'r')as f:
                json_dict = json.load(f)
                android_text(json_dict, name_count)
                # android_null(json_dict, name_count)
                # android_image(json_dict, name_count)
                # android_c_o(json_dict, name_count)
                print(name_count)


