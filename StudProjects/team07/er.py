import subprocess

import matplotlib.pyplot as plt
from joblib import load

from utils import *

# clf = load('model/model_cafe')
clf = load('model/model_ck')


def generate_aus():
    out_dir = "./out/AUs"
    out_file = "cam_vid"
    program_bin = "./OpenFace/build/bin/FeatureExtraction"

    # for windows users:
    # programPath = "OpenFace"
    # cmdCommand = "cd "+programPath+" & "+"FaceLandmarkImg.exe -aus -out_dir ."+outDir+"  -f ."+imagePath +" > logs"

    subprocess.call([program_bin, '-aus', '-device', '0', '-out_dir', out_dir, '-of', out_file])


def get_emotions():
    frame_emotions = []
    frame_timestamp = []
    with open(os.path.join('./out/AUs/', "cam_vid.csv")) as fp:
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
    last_second = np.ceil(frame_timestamp[-1])
    plt.xticks(np.arange(0, last_second, last_second / 10))
    plt.scatter(frame_timestamp[2:-1:20], frame_emotions[2:-1:20])
    plt.show()
    plt.hist(frame_emotions)
    plt.show()


def main():
    generate_aus()
    get_emotions()


main()
