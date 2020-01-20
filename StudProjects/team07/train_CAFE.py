from utils import *


def get_data():
    data = {}

    cafe_path = './data/cafe'
    for emotion in os.listdir(cafe_path):
        aus_path = os.path.join(cafe_path, emotion, 'out', emotion + '.csv')
        with open(aus_path) as fp:
            column_names = fp.readline().split(", ")
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
                emotion_aus = data[emotion] if emotion in data else []
                emotion_aus.append(aus)
                data[emotion] = emotion_aus
    return data


def main():
    data = get_data()
    train(data, 'model/model_cafe')


main()
