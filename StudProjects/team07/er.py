from test import *

cafe_clf = load('model/model_cafe')
# ck_clf = load('model/model_ck')


def generate_aus():
    out_dir = "./out/AUs"
    out_file = "cam_vid"
    logs_file = open('./out/logs', 'w')

    subprocess.call([openface_path, '-aus', '-device', '0', '-out_dir', out_dir, '-of', out_file], stdout=logs_file)


def get_emotions(clf):
    frame_emotions = []
    frame_timestamp = []
    with open(os.path.join('./out/AUs/', "cam_vid.csv")) as fp:
        column_names = fp.readline().split(", ")
        #next(fp)
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


def printMenu():
    print("Select mode: ")
    print("1. Test")
    print("2. Run")

    print("\n")


def main():
    while (True):
        printMenu()
        mode = input("Mode: ")

        if mode == "1":
            test()
        elif mode == "2":
            generate_aus()
            get_emotions(ck_clf)
        elif mode == "q":
            break
        else:
            print("Not a valid option")

        print("Finished! \n")


main()
