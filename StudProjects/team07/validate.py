import subprocess

from joblib import load

from utils import *

clf = load('model/model_cafe')
# clf = load('model_ck')


def generate_aus(directory, file):
    out_dir = "./out/AUs"
    out_file = os.path.join(directory, file) + ".csv"

    programPath = "./OpenFace/build/bin/"

    # for windows users:
    # programPath = "OpenFace"
    # cmdCommand = "cd "+programPath+" & "+"FaceLandmarkImg.exe -aus -out_dir ."+out_dir+"  -f ."+imagePath +" > logs"

    subprocess.call([programPath + 'FeatureExtraction', '-f', os.path.join(directory, file), '-out_dir', out_dir, '-of', out_file])


def get_emotions(directory, file):
    frame_emotions = []
    frame_timestamp = []
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
    show_statistics(frame_timestamp, frame_emotions)


def main():
    directory = "data/emoreact/Data/Test"
    file = "ANNOYING_ORANGE83_2.mp4"
    generate_aus(directory, file)
    get_emotions(directory, file)


main()
