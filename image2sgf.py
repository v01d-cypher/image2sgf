#!/usr/bin/env python

import Image
import os
import string
import sys

image_dir = sys.argv[1]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BORDER = 9
INTERVAL = 19

# use a small offset from intersection to make sure we don't grab a
# black pixel from the grid line as opposed to a black pixel from a stone
OFFSET = 3

# TL = Top Left , TR = Top Right
# BL = Bottom Left , BR = Bottom Right
# the corner you want the image flipped from
ORIGIN_CORNER = 'TR'
# the corner you want the image flipped to
TARGET_CORNER = 'TL'


def transpose_image(image, x_lines, y_lines):
    transpose_matrix = {
        ('TL', 'TR'): 'V',
        ('TL', 'BL'): 'H',
        ('TL', 'BR'): 'HV',

        ('TR', 'TL'): 'V',
        ('TR', 'BL'): 'HV',
        ('TR', 'BR'): 'H',

        ('BL', 'TL'): 'H',
        ('BL', 'TR'): 'HV',
        ('BL', 'BR'): 'V',

        ('BR', 'TL'): 'HV',
        ('BR', 'TR'): 'H',
        ('BR', 'BL'): 'V'}

    if TARGET_CORNER == 'TL':
        x_string = y_string = string.ascii_letters
    elif TARGET_CORNER == 'TR':
        x_string = string.ascii_letters[19 - x_lines:19]
        y_string = string.ascii_letters
    elif TARGET_CORNER == 'BL':
        x_string = string.ascii_letters
        y_string = string.ascii_letters[19 - y_lines:19]
    elif TARGET_CORNER == 'BR':
        x_string = string.ascii_letters[19 - x_lines:19]
        y_string = string.ascii_letters[19 - y_lines:19]

    for instruction in transpose_matrix[(ORIGIN_CORNER, TARGET_CORNER)]:
        if instruction == 'H':
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if instruction == 'V':
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

    return image, x_string, y_string


for root, dir, files in os.walk(image_dir):
    for image in files:
        path = os.path.join(root, image)
        try:
            im = Image.open(path)
        except:
            print("Cannot open '{}'. Not supported or not an image file".format(path))
            continue

        width, height = im.size
        x_lines = width / INTERVAL
        y_lines = height / INTERVAL

        im, x_string, y_string = transpose_image(im, x_lines, y_lines)

        # deduct 1 from total lines because first line starts on offset
        x_lines = x_lines - 1
        y_lines = y_lines - 1

        rgbimg = im.convert('RGB')
        pixels = rgbimg.load()

        coords = {
            'AB': [],
            'AW': []}

        index_x_string = 0
        for x in range(BORDER, (INTERVAL * x_lines) + INTERVAL, INTERVAL):
            index_y_string = 0
            for y in range(BORDER, (INTERVAL * y_lines) + INTERVAL, INTERVAL):
                # get pixel using no offset:
                #   if it's white, then it's a white stone
                #   if it's black:
                #     get pixel using offset:
                #       if it's black, then it's a black stone
                #       else it's an empty intersection
                point = pixels[x, y]
                if point == WHITE:
                    coords['AW'].append('[{}{}]'.format(x_string[index_x_string], y_string[index_y_string]))
                else:
                    point = pixels[x + OFFSET, y + OFFSET]
                    if point == BLACK:
                        coords['AB'].append('[{}{}]'.format(x_string[index_x_string], y_string[index_y_string]))

                index_y_string += 1
            index_x_string += 1

        with open('{}.sgf'.format(os.path.splitext(path)[0]), 'w') as f:
            f.write('(;GM[1]FF[4]SZ[19]\n')
            f.write('AB{}\n'.format(''.join(sorted(coords['AB']))))
            f.write('AW{}\n'.format(''.join(sorted(coords['AW']))))
            f.write(')\n')
