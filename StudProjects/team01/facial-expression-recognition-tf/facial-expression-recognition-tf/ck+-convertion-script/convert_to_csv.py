"""
Converts the CK+ dataset to FER-2013 .csv style dataset.
Each line would have (label, 2304 grayscale pixels).
"""
import sys
import os
import csv
import glob
from PIL import Image

from keras.preprocessing.image import img_to_array
from keras.models import load_model
import imutils
import cv2
import numpy as np
import tensorflow as tf

# parameters for loading data and images
detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)

#Useful function
def createFileList(myDir, format='.txt'):
    fileList = []
    print(myDir)
    for root, dirs, files in os.walk(myDir, topdown=False):
        for name in files:
            if name.endswith(format):
                fullName = os.path.join(root, name)
                fileList.append(fullName)
    return fileList

def createPicturePaths(labelPaths):
    fileList = []
    for path in labelPaths:
        picturePath = path.replace('Emotion', 'cohn-kanade-images').replace('_emotion.txt', '.png')
        fileList.append(picturePath)
    return fileList
    
# load all the labels
myLabelsPaths = createFileList('ck+-original/Emotion')
myPicturePaths = createPicturePaths(myLabelsPaths)

with open("img_pixels.csv", 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['emotion', 'pixels', 'Usage'])

ckpToFER2013EmotionConvertor = [
    [6], # Here, Neutral is 0, but in FER-2013 it is 6
    [0], # Here, Anger is 1, but in FER-2013 it is 0
    [None], # Contempt is not in FER-2013
    [1], # Here, Disgust is 3, but in FER-2013 it is 1
    [2], # Here, Fear is 4, but in FER-2013 it is 2
    [3], # Here, Happy is 5, but in FER-2013 it is 3
    [4], # Here, Sadness is 6, but in FER-2013 it is 4
    [5], # Here, Surprise is 7, but in FER-2013 it is 5
]

for picture, label in zip(myPicturePaths, myLabelsPaths):
    print(picture, label)
    frame = cv2.imread(picture)
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))
    if len(faces) > 0:
        (fX, fY, fW, fH) = faces[0]
        # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
        # the ROI for classification via the CNN
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = img_to_array(roi)
        roi = roi.astype("int")
        roi = roi.flatten()
        string_representation = ' '.join(str(x) for x in roi)
        #print(string_representation)
        
        # Read emotion label
        label_file = open(label)
        emotion = label_file.read().strip()
        emotion_number = int(eval(emotion))
        print(emotion_number)
        
        if emotion_number == 2:
            continue
        else:
            new_emotion_number = ckpToFER2013EmotionConvertor[emotion_number][0]
            print(new_emotion_number)
            row = [new_emotion_number, string_representation, '']    
            with open("img_pixels.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
