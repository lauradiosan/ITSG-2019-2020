import subprocess

from joblib import load

from utils import *

cafe_clf = load('model/model_cafe')
ck_clf = load('model/model_ck')

# 1- Curiosity
# 2- Uncertainty
# 3- Excitement
# 4- Happiness
# 5- Surprise
# 6- Disgust
# 7- Fear
# 8- Frustration
# 9- Valence

ck_emotion_names = ['neutral', 'angry', 'contempt', 'disgust', 'fearful', 'happy', 'sad', 'surprise']
emoreact_emotion_names = [None, None, None, 'happy', 'surprise', 'disgust', 'fearful', None]


def generate_aus(directory, file):
    out_dir = "./out/AUs"
    out_file = os.path.join(directory, file) + ".csv"
    logs_file = open('./out/logs', 'w')

    subprocess.call([openface_path, '-aus', '-f', os.path.join(directory, file), '-out_dir', out_dir, '-of', out_file], stdout=logs_file)


def get_emotions_from_video(directory, file, clf, generate_statistics=False):
    frame_emotions = []
    frame_timestamp = []
    # generate_aus(directory, file)
    with open(os.path.join('./out/AUs/', directory, file) + ".csv") as fp:
        column_names = fp.readline().split(", ")
        next(fp)
        for line in fp:
            aus = [0] * len(all_aus)
            column_values = line.split(", ")
            for i in range(len(column_names)):
                name = column_names[i]
                if name[-1:] == "c":
                    if column_values[i] == "1.00":
                        au_string = name[2:4]
                        auStringNewFormat = float(au_string[1]) if au_string[0] == "0" else float(au_string)
                        if auStringNewFormat in all_aus:
                            index = all_aus.index(auStringNewFormat)
                            aus[index] = 1
            predicted_emotion = clf.predict([aus])
            frame_emotions.append(predicted_emotion[0])
            frame_timestamp.append(float(column_values[2]))

    if generate_statistics:
        show_statistics(frame_timestamp, frame_emotions)
    return frame_emotions


def get_top_emotions(file, clf):
    directory = 'data/emoreact/Data/Train'

    emotions = get_emotions_from_video(directory, file, clf)
    mode_top = max(set(emotions), key=emotions.count)

    emotions = list(filter(lambda x: x != mode_top, emotions))
    mode_second = max(set(emotions), key=emotions.count) if emotions.__len__() > 0 else mode_top

    return [mode_top, mode_second]


# labeles = [1, 1, 1, 1, 1, 1, 1, 1, 1.1111]
# emotions = ['happy', 'sad']
def get_match(labeles, emotions):
    match = None
    for emotion in emotions:
        if emoreact_emotion_names.__contains__(emotion):
            index = emoreact_emotion_names.index(emotion)
            if (labeles[index] != None): match = match or labeles[index] == '1'
    return match


def test_on_emoreact(clf):
    matches = []
    labels_file_location = 'data/emoreact/Labels/train_labels.text'
    names_file_location = 'data/emoreact/Train_names.txt'

    labels_lines = open(labels_file_location).readlines()
    file_names_lines = open(names_file_location).readlines()

    for index, line in enumerate(file_names_lines):
        file_name = line.replace('\'\'', '\'').replace('\n', '')[1:-1]
        print(file_name)
        emotions = get_top_emotions(file_name, clf)
        labels = labels_lines[index][0:15].split(',')

        match = get_match(labels, emotions)
        matches.append(match)

    return ["Correct" if x == True else "Incorrect" if x == False else "N/A" for x in matches]


def extract_emotion(path):
    emotion_file = open(path)
    emotion = float(emotion_file.readline())
    emotion_file.close()
    return str(emotion)


# S005_001_00000011_emotion.txt
# S005_001_00000001.png
def test_on_ck(clf):
    matches = []
    for subdir, dirs, files in os.walk('data/ck/Emotion/'):
        for file in files:
            emotion_path = os.path.join(subdir, file)
            emotion = ck_emotion_names[int(float(extract_emotion(emotion_path)))]

            image_dir = subdir.replace('Emotion', 'images')
            image_file = file.replace('_emotion.txt', '.png')
            print(image_file)
            # generate_aus(image_dir, image_file)

            aus_file = os.path.join('./out/AUs/', image_dir, image_file) + ".csv"
            with open(aus_file) as f:
                column_names = f.readline().split(", ")
                aus = [0] * len(all_aus)
                column_values = f.readline().split(", ")
                for i in range(len(column_names)):
                    name = column_names[i]
                    if name[-1:] == "c":
                        if column_values[i] == "1.00":
                            au_string = name[2:4]
                            auStringNewFormat = float(au_string[1]) if au_string[0] == "0" else float(au_string)
                            if auStringNewFormat in all_aus:
                                index = all_aus.index(auStringNewFormat)
                                aus[index] = 1
            predicted_emotion = clf.predict([aus])[0]
            match = predicted_emotion == emotion
            matches.append(str(match))
    return matches


def test():
    cafe_matches = test_on_emoreact(cafe_clf)
    ck_matches = test_on_emoreact(ck_clf)

    plt.hist([cafe_matches, ck_matches], label=['cafe', 'ck'])

    plt.legend(loc='upper center')
    plt.show()
