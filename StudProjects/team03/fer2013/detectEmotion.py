# load json and create model
from __future__ import division
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import model_from_json
import numpy
import os
import numpy as np
import sys
from PIL import Image

import warnings

warnings.filterwarnings("ignore")

labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def die(error):
    print(error)
    exit(1)


with open('generated.json', 'r') as json_file:
    loaded_model_json_caffe = json_file.read()

loaded_model_caffe = model_from_json(loaded_model_json_caffe)
loaded_model_caffe.load_weights("generated.h5")

with open('fer.json', 'r') as json_file:
    loaded_model_json_fer = json_file.read()

loaded_model_fer = model_from_json(loaded_model_json_fer)
loaded_model_fer.load_weights("fer.h5")


def recognise(file_name, type='caffe'):
    loaded_model = loaded_model_caffe if type == 'caffe' else loaded_model_fer
    new_array = []
    try:
        img = Image.open(os.path.abspath(file_name))
        img = img.convert("L")
        img = img.resize((48, 48))
        img_array = np.array(img)
        for i in range(len(img_array)):
            new_array.append(np.reshape(img_array[i], (len(img_array[i]), 1)))
        new_array = np.array(new_array)
    except IOError:
        return {}

    values = loaded_model.predict(np.array([new_array]))[0]
    indexs = [i for i in range(0, 7)]
    indexs = sorted(indexs, key=lambda x: values[x], reverse=True)
    dic = {}
    for i in indexs:
        dic[labels[i]] = int(values[i] * 10000) / 100
    return dic


if __name__ == '__main__':
    dic = recognise(sys.argv[1])
    for (key, value) in dic.items():
        print("{0}: {1}%".format(key, value))
