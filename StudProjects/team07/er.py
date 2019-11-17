from joblib import load

from utils import *

# clf = load('model_cafe')
clf = load('model_ck')


def generate_aus():
    outDir = "./test/AUs"
    programPath = "./OpenFace/build/bin/"
    cmdCommand = programPath + "FeatureExtraction -aus -out_dir " + outDir + " -of cam_vid  -device 0 > logs"

    # for windows users:
    # programPath = "OpenFace"
    # cmdCommand = "cd "+programPath+" & "+"FaceLandmarkImg.exe -aus -out_dir ."+outDir+"  -f ."+imagePath +" > logs"

    os.system(cmdCommand)


def get_emotions():
    for file in os.listdir('./test/AUs/'):
        if file.endswith(".csv"):
            with open(os.path.join('./test/AUs/', file)) as fp:
                columnNames = fp.readline().split(", ")
                next(fp)
                for line in fp:
                    aus = [0] * len(all_aus)
                    columnValues = line.split(", ")
                    for i in range(len(columnNames)):
                        name = columnNames[i]
                        if name[-1:] == "c":
                            if columnValues[i] == "1.00":
                                auString = name[2:4]
                                auStringNewFormat = float(auString[1]) if auString[0] == "0" else float(auString)
                                if auStringNewFormat in all_aus:
                                    index = all_aus.index(auStringNewFormat)
                                    aus[index] = 1
                    predicted_emotion = clf.predict([aus])
                    print()
                    print("EMOTION: " + predicted_emotion[0])


def main():
    generate_aus()
    get_emotions()


main()
