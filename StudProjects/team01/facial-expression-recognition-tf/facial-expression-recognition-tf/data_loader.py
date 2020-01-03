"""
Data loader reads a .csv file and creates a train and test dataset for our model to be trained with.
Requirements for the .csv file:
- it should have lines with label, followed by an array of 2304 (48x48) grayscale pixels, separated by spaces.
- e.g.: 1, 201 103 78 ... 101
The train images will be in variable: xtrain
The train labels will be in variable: ytrain
The test images will be in variable: xtest
The test labels will be in variable: ytest
"""
import pandas as pd
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

dataset_path = 'datasets/fer2013/private_test_fer2013.csv'

image_size = (48, 48)

"""
Reads .csv file and returns the tuple (faces, emotions).
"""
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
    faces = np.expand_dims(faces, -1)
    emotions = pd.get_dummies(data['emotion']).as_matrix()
    return faces, emotions
 
def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x
 
faces, emotions = load_fer2013()
faces = preprocess_input(faces)
xtrain, xtest, ytrain, ytest = train_test_split(faces, emotions, test_size=0.2, shuffle=True)
