# encoding:utf-8
# @Author :ZQY
from convert_points_image import img

try1 = img('./images/123.jpg')
try1.RGB_to_points(40, 40, converse=False, save_filename='./images/convert1.txt')

