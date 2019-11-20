from PIL import Image
import numpy as np
import sys
import os
import csv
import glob

# from the ck+ dataset, which is placed under path "ck+-original/Emotion",
# this script takes the paths of all the labeled images and converts
# the labeled images and labes into a csv file named "img_pixels.csv"

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
    img_file = Image.open(picture)
    img_file = img_file.resize((48, 48), Image.ANTIALIAS)
    #img_file.show()

    # get original image parameters...
    width, height = img_file.size
    format = img_file.format
    mode = img_file.mode

    # Make image Greyscale
    img_grey = img_file.convert('L')
    #img_grey.save('result.png')
    #img_grey.show()

    # Save Greyscale values
    value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
    value = value.flatten()
    string_representation = ' '.join(str(x) for x in value)
    #print(string_representation)
    
    # Read emotion label
    label_file = open(label)
    emotion = label_file.read().strip()
    emotion_number = int(eval(emotion))
    print(emotion_number)
    
    if emotion_number == 2:
        continue
    else:
        #if emotion_number != 5:
        #    continue
        new_emotion_number = ckpToFER2013EmotionConvertor[emotion_number][0]
        print(new_emotion_number)
        row = [new_emotion_number, string_representation, '']    
        with open("img_pixels.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)