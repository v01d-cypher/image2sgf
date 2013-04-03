#!/usr/bin/env python

import Image
import os
import string
import sys

image_dir = sys.argv[1]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

offset = 13
interval = 19


for root, dir, files in os.walk(image_dir):
    for image in files:
        path = os.path.join(root, image)
        try:
            im = Image.open(path)
        except:
            print("Cannot open '{}'. Not supported or not an image file".format(path))
            continue

        #These images are on the top-right of board. Flip image to make it top-left.
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        width, height = im.size
        x_lines = width / interval
        y_lines = height / interval

        # Get letter coordinates for top-right of board
        #x_string_coord = string.ascii_letters[19 - x_lines:19]
        #y_string_coord = string.ascii_letters[:y_lines]

        # Get letter coordinates for top-left of board
        x_string_coord = y_string_coord = string.ascii_letters

        #deduct 1 from total lines because first line starts on offset
        x_lines = x_lines - 1
        y_lines = y_lines - 1

        rgbimg = im.convert('RGB')
        pix = rgbimg.load()

        coords = {
            'AB': [],
            'AW': []}

        xc = 0
        yc = 0
        for x in range(offset, (interval * x_lines) + interval, interval):
            yc = 0
            for y in range(offset, (interval * y_lines) + interval, interval):
                p = pix[x, y]
                if p == BLACK:
                    coords['AB'].append('[{}{}]'.format(x_string_coord[xc], y_string_coord[yc]))
                if p == WHITE:
                    coords['AW'].append('[{}{}]'.format(x_string_coord[xc], y_string_coord[yc]))
                yc += 1
            xc += 1

        with open('{}.sgf'.format(os.path.splitext(path)[0]), 'w') as f:
            f.writelines('(;GM[1]FF[4]SZ[19]')
            f.writelines('AB{}'.format(''.join(sorted(coords['AB']))))
            f.writelines('AW{}'.format(''.join(sorted(coords['AW']))))
            f.writelines(')')
