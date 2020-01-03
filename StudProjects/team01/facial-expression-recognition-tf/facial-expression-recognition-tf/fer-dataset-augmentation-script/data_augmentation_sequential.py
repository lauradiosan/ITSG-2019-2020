"""
Augments a FER-2013 like dataset with several kind of noise.
"""
import cv2
import csv
import pandas as pd
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
import imgaug as ia
import imgaug.augmenters as iaa

dataset_path = 'train_fer2013.csv'
#dataset_path = 'img_pixels.csv'
image_size = (48, 48)
 
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

# original
original, original_emotions = load_fer2013()

# add original pictures to the augmented_dataset.csv file
with open("augmented_dataset.csv", 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['emotion', 'pixels', 'Usage'])
    
    string_representation = []
    for img in original:
        img = img.flatten()
        img = img.astype('int')
        str_repr = ' '.join(str(x) for x in img)
        string_representation.append(str_repr)
    
    for picture, label in zip(string_representation, original_emotions):
        row = [label, picture, '']  
        writer.writerow(row)

# enlist the augmentation functions
augmentation_functions = [
    #iaa.Add((-50, 50)),
    iaa.AdditiveGaussianNoise(scale=0.07*255),
    iaa.Multiply((0.25, 1.50)),
    iaa.SaltAndPepper(0.03),
    iaa.GaussianBlur(0.50),
    iaa.Clouds()
]

# add augmented pictures to the augmented_dataset.csv file
with open("augmented_dataset.csv", 'a', newline='') as f:
    writer = csv.writer(f)
    for aug_function in augmentation_functions:
        augmented_dataset = aug_function(images=original)
        augmented_dataset = augmented_dataset.astype('int')

        string_representation = []
        for img in augmented_dataset:
            img = img.flatten()
            str_repr = ' '.join(str(x) for x in img)
            string_representation.append(str_repr)
        
        for picture, label in zip(string_representation, original_emotions):
            row = [label, picture, '']  
            writer.writerow(row)

#print(string_representation[7])
#im = Image.fromarray(all_images[7])
#im.show()
