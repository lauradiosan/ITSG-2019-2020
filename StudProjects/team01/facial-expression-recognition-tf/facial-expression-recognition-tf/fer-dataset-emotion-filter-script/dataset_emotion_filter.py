from PIL import Image
import numpy as np
import sys
import os
import csv
import glob
import pandas as pd
import cv2

dataset_path = 'img_pixels.csv'

image_size=(48,48)

def load_fer2013():
    data = pd.read_csv(dataset_path)
    pixels = data['pixels'].tolist()
    width, height = 48, 48
    faces = []
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.asarray(face).reshape(width, height)
        face = cv2.resize(face.astype('uint8'), image_size)
        faces.append(face.astype('float32'))
    faces = np.asarray(faces)
    #emotions = pd.get_dummies(data['emotion']).as_matrix()
    emotions = data['emotion']
    return faces, emotions

original, original_emotions = load_fer2013()

datasetEmotionLabelMapper = [
    [0], # Angry stays 0
    [None], # Disgust is removed
    [1], # Fear becomes 1
    [2], # Happy becomes 2
    [3], # Sad becomes 3
    [4], # Surprise becomes 4
    [5], # Neutral becomes 5
]

with open("filtered_%s" % dataset_path, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['emotion', 'pixels', 'Usage'])
    
    string_representation = []
    for img in original:
        img = img.flatten()
        img = img.astype('int')
        str_repr = ' '.join(str(x) for x in img)
        string_representation.append(str_repr)
    
    for picture, label in zip(string_representation, original_emotions):
        newLabel = datasetEmotionLabelMapper[label][0]
        if newLabel is not None:            
            row = [newLabel, picture, '']  
            writer.writerow(row)