import os
from datetime import datetime

import cv2
import numpy as np
from sklearn.svm import SVC

emotionNames = ['neutral', 'anger', 'contempt', 'disgust', 'fear', 'happy', 'sadness', 'surprise']
allAus = [1.0, 2.0, 4.0, 5.0, 6.0, 7.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 20.0, 21.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 30.0, 31.0, 34.0, 38.0, 39.0,
          43.0, 45.0, 54.0, 62.0, 63.0, 64.0]
clf = SVC(gamma='auto')


def train(data):
    aus = []
    emotions = ([])
    for emotion in data.keys():
        for au in data[emotion]:
            aus.append(au)
            emotions.append(emotion)

    clf.fit(np.array(aus), np.array(emotions))


def get_data(path, normalized):
    data = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            emotion_path = os.path.join(subdir, file)
            facs_path = os.path.join(subdir.replace('Emotion', 'FACS'), file.replace('emotion', 'facs'))

            emotion = extract_emotion(emotion_path)
            if normalized:
                facs = extract_normalized_facs_without_intensity(facs_path)
            else:
                facs = extract_facs_without_intensity(facs_path)

            all_facs = data[emotion] if emotion in data else []
            all_facs.append(facs)
            data[emotion] = all_facs
    return data


def extract_emotion(path):
    emotion_file = open(path)
    emotion = float(emotion_file.readline())
    emotion_file.close()
    return str(emotion)


def extract_facs_with_intensity(path):
    facs_file = open(path)
    facs = {}
    for line in facs_file.readlines():
        au = float(line.replace('   ', '', 1).replace('  ', '', 1).split(' ')[0])
        intensity = float(line.replace('   ', '', 1).replace('  ', '', 1).split(' ')[1])
        facs[str(au)] = str(intensity)
    facs_file.close()
    return facs


def extract_normalized_facs_without_intensity(path):
    facs_file = open(path)
    facs = [0 for i in range(35)]
    for line in facs_file.readlines():
        au = float(line.replace('   ', '', 1).replace('  ', '', 1).split(' ')[0])
        facs[allAus.index(au)] = 1
    facs_file.close()
    return facs


def extract_facs_without_intensity(path):
    facs_file = open(path)
    facs = []
    for line in facs_file.readlines():
        au = float(line.replace('   ', '', 1).replace('  ', '', 1).split(' ')[0])
        facs.append(au)
    facs_file.close()
    return facs


def test(path):
    data = get_data(path, True)
    for emotion in data.keys():
        for aus in data[emotion]:
            predicted_emotion = clf.predict([aus])
            print("P: " + emotionNames[int(predicted_emotion[0].split(".")[0])] + "  R: " + emotionNames[int(emotion.split(".")[0])])


def getEmotion(image):
    with open('./test/AUs/' + image + '.csv') as fp:
        "AU12_c"
        aus = [0] * len(allAus)
        columnNames = fp.readline().split(", ")
        columnValues = fp.readline().split(", ")
        for i in range(len(columnNames)):
            name = columnNames[i]
            if name[-1:] == "c":
                if columnValues[i] == "1.0":
                    auString = name[2:4]
                    auStringNewFormat = float(auString[1]) if auString[0] == "0" else float(auString)
                    if auStringNewFormat in allAus:
                        index = allAus.index(auStringNewFormat)
                        aus[index] = 1
    predicted_emotion = clf.predict([aus])
    print()
    print("EMOTION: " + emotionNames[int(predicted_emotion[0].split(".")[0])])


def captureImage():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)

        if k % 256 == 32:
            # SPACE pressed
            img_name = "test/images/image.jpg"
            cv2.imwrite(img_name, frame)
            break
    cam.release()
    cv2.destroyAllWindows()


def generateAUs():
    outDir = "./test/AUs"
    imagePath = "./test/images/image.jpg"
    programPath = "./OpenFace/build/bin/"
    cmdCommand = programPath + "FaceLandmarkImg -aus -out_dir " + outDir + "  -f " + imagePath  + " > logs"

    # for windows users:
    # programPath = "./OpenFace/"
    # cmdCommand = programPath+"FaceLandmarkImg.exe -aus -out_dir "+outDir+"  -f "+imagePath +" > logs"

    os.system(cmdCommand)


def main():
    data = get_data('Emotion/', True)
    train(data)
    while True:
        captureImage()
        generateAUs()
        getEmotion('image')


main()
