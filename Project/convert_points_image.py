# encoding:utf-8
# @Author :ZQY
# pillow: https://blog.csdn.net/lancerdaidai/article/details/110634935
# pillow official: https://pillow.readthedocs.io/en/latest/handbook/concepts.html#bands
import os

from PIL import Image


class img:
    def __init__(self, filename: str):
        self.im = Image.open(filename)
        self.filename = filename

    def smooth_points(self, image0, level=5):
        im = image0.copy()
        w, l = im.size
        im_load = im.load()

        def eval0(s):
            s0, s1 = s[0], s[1]
            count0, count255 = 0, 0
            add_list = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
            for add in add_list:
                if 0 <= s0 + add[0] < w and 0 <= s1 + add[1] < l:
                    if im_load[s0 + add[0], s1 + add[1]] == 0:
                        count0 += 1
                    else:
                        count255 += 1
            return count0, count255

        for i in range(w):
            for j in range(l):
                temp = eval0([i, j])
                if temp[0] >= temp[1] + level:
                    im_load[i, j] = 0
                elif temp[0] <= temp[1] - level:
                    im_load[i, j] = 255

        return im

    def convert_unicode(self, mat0):
        '''
        8个像素点转化成盲文
        :param mat0: 4*2像素点
        :return: 盲文Unicode
        '''
        if len(mat0) != 4 or len(mat0[0]) != 2:
            raise ValueError('错错错')

        bin_str = str(mat0[3][1]) + str(mat0[3][0]) + str(mat0[2][1]) + str(mat0[1][1]) + \
                  str(mat0[0][1]) + str(mat0[2][0]) + str(mat0[1][0]) + str(mat0[0][0])
        dec_num = int(bin_str, 2)
        # hex_str = hex(dec_num)[2:]
        return chr(int('2800', 16) + dec_num)

    def RGB_to_points(self, width, length, converse=False, save_filename=''):
        '''
        把彩色图变成点阵图
        :param save_filename: 如果保存，填写保存位置，默认不保存
        :param length: 长要求被2整除
        :param width: 宽要求被4整除
        :param converse: 阴文阳文互换
        :return: show image
        '''
        im = self.im.resize((length, width))
        im = im.convert('1')
        # im = self.smooth_points(im)
        # im = self.smooth_points(im)
        im.show()
        im.save(self.filename[:-4]+'convert'+'.jpg')
        # os.system('pause')

        im_load = im.load()
        if width % 4 != 0 or length % 2 != 0:
            raise ValueError('长宽不合适')
        w, l = width // 4, length // 2
        res = ''
        for j in range(w):
            for i in range(l):
                tmp = [[0, 0] for _ in range(4)]
                for i0 in range(2):
                    for j0 in range(4):
                        if not converse:
                            tmp[j0][i0] = 1 if im_load[2 * i + i0, 4 * j + j0] else 0
                        else:
                            tmp[j0][i0] = 0 if im_load[2 * i + i0, 4 * j + j0] else 1
                res += self.convert_unicode(tmp)
            res += '\n'

        # 保存点阵
        print(res)
        if save_filename:
            with open(save_filename, 'w', encoding='utf-8') as fl:
                fl.write(res)


if __name__ == "__main__":
    try1 = img('./images/123.jpg')
    try1.RGB_to_points(40, 40, converse=True, save_filename='./images/convert1.txt')
