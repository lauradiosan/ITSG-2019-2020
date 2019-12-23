import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from joblib import dump
from sklearn.svm import LinearSVC

openface_path = input("OpenFace path: ")
all_aus = [1.0, 2.0, 4.0, 5.0, 6.0, 7.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 20.0, 21.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 30.0, 31.0, 34.0, 38.0, 39.0,
           43.0, 45.0, 54.0, 62.0, 63.0, 64.0]

emotion_names = ['neutral', 'angry', 'contempt', 'disgust', 'fearful', 'happy', 'sad', 'surprise']


def train(data, model_name):
    clf = LinearSVC()
    aus = []
    emotions = ([])
    for emotion in data.keys():
        for au in data[emotion]:
            aus.append(au)
            emotions.append(emotion)

    clf.fit(np.array(aus), np.array(emotions))
    dump(clf, model_name)


def generate_cafe_aus():
    open_face_path = "./OpenFace/build/bin/"
    base_path = './data/cafe'
    for folder in os.listdir(base_path):
        print("Starting extracting data for emotion: " + folder)
        emotion_folder_path = os.path.join(base_path, folder)
        outDir = os.path.join(emotion_folder_path, 'out')
        logs_file = open('./out/logs', 'w')

        subprocess.call([openface_path, '-aus', '-out_dir', outDir, '-fdir', emotion_folder_path], stdout=logs_file)

        #open_face_command = open_face_path + "FeatureExtraction -aus -out_dir " + outDir + " -fdir " + emotion_folder_path + " > logs"
        #os.system(open_face_command)
        print("Ended extracting data for emotion: " + folder)


def show_statistics(timestamps, emotions):
    last_second = np.ceil(timestamps[-1])
    plt.subplot(2, 1, 1)
    plt.xticks(np.arange(0, last_second, last_second / 10))
    plt.scatter(timestamps[2:-1:20], emotions[2:-1:20])

    plt.subplot(2, 1, 2)
    plt.hist(emotions)
    plt.show()
