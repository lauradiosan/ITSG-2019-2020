import pandas as pd
import cv2
import csv
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
import imgaug as ia
import imgaug.augmenters as iaa

#dataset_path = 'fer2013/public_test_fer2013.csv'
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

# original
original, original_emotions = load_fer2013()

# flipped
flip = iaa.Fliplr(1)
flipped, flipped_emotions = flip(images=original), original_emotions

# add(original + flipped)
add = iaa.Add((-50, 50))
added, added_emotions = add(images=np.concatenate((original, flipped))), np.concatenate((original_emotions, flipped_emotions))

# additive_gaussian_noise(original + flipped)
additive_gaussian_noise = iaa.AdditiveGaussianNoise(scale=0.07*255)
additive_gaussian_noise_applied, additive_gaussian_noise_applied_emotions = additive_gaussian_noise(images=np.concatenate((original, flipped))), np.concatenate((original_emotions, flipped_emotions))

# multiply (original + flipped)
multiply = iaa.Multiply((0.25, 1.50))
multiplied, multiplied_emotions = multiply(images=np.concatenate((original, flipped))), np.concatenate((original_emotions, flipped_emotions))

# salt_and_pepper (original + flipped)
salt_and_pepper = iaa.SaltAndPepper(0.03)
salt_and_pepper_applied, salt_and_pepper_applied_emotions = salt_and_pepper(images=np.concatenate((original, flipped))), np.concatenate((original_emotions, flipped_emotions))

# guassian_blur (original + flipped)
guassian_blur = iaa.GaussianBlur(0.50)
guassian_blur_applied, guassian_blur_applied_emotions = guassian_blur(images=np.concatenate((original, flipped))), np.concatenate((original_emotions, flipped_emotions))

# clouds (original + flipped)
clouds = iaa.Clouds()
clouds_applied, clouds_applied_emotions = clouds(images=np.concatenate((original, flipped))), np.concatenate((original_emotions, flipped_emotions))

all_images = np.concatenate((original, flipped, added, additive_gaussian_noise_applied, multiplied, salt_and_pepper_applied, guassian_blur_applied, clouds_applied))
all_images_emotions = np.concatenate((original_emotions, flipped_emotions, added_emotions, additive_gaussian_noise_applied_emotions, multiplied_emotions, salt_and_pepper_applied_emotions, guassian_blur_applied_emotions, clouds_applied_emotions))

all_images = all_images.astype('int')

string_representation = []
for img in all_images:
    img = img.flatten()
    str_repr = ' '.join(str(x) for x in img)
    string_representation.append(str_repr)


with open("augmented_dataset.csv", 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['emotion', 'pixels', 'Usage'])
    for picture, label in zip(string_representation, all_images_emotions):
        row = [label, picture, '']  
        writer.writerow(row)


#print(string_representation[7])
#im = Image.fromarray(all_images[7])
#im.show()
