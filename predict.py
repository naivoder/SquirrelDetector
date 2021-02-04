#! /usr/bin/env python

import os
import logging
import argparse

import cv2
import numpy as np
from tqdm import tqdm
from utils.models import Yolov4

print('-----------------')
print('SQUIRREL DETECTOR')
print('-----------------')

# DISABLE TENSORFLOW INFO MESSAGES
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)

def _main_(args):
    input_path = args.input
    output_path = args.output
    os.makedirs(output_path, exist_ok=True)

    model = Yolov4(weight_path='utils/squirrel.h5',
                         class_name_path='utils/classes.txt')

    image_paths = []

    if os.path.isdir(input_path): 
        for inp_file in os.listdir(input_path):
            image_paths += [input_path + inp_file]
    else:
        image_paths += [input_path]

    image_paths = [inp_file for inp_file in image_paths if (inp_file[-4:] in ['.jpg', '.png', 'JPEG'])]
    imgs = np.array(image_paths)
    
    # the main loop
    for i in tqdm(range(len(imgs))):
        out = model.predict(imgs[i], random_color=True)
        out_img = cv2.cvtColor(out[0], cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(output_path, str(i) + '.png'), out_img)         

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Detect Squirrels!')
    argparser.add_argument('-i', '--input', help='path to an image, or directory of images')    
    argparser.add_argument('-o', '--output', default='output/', help='path to output directory')   
    
    args = argparser.parse_args()
    _main_(args)