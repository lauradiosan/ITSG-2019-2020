from utils import *


def get_data(path, normalized):
    data = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            emotion_path = os.path.join(subdir, file)
            facs_path = os.path.join(subdir.replace('Emotion', 'FACS'), file.replace('emotion', 'facs'))

            emotion = emotion_names[int(float(extract_emotion(emotion_path)))]
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
        facs[all_aus.index(au)] = 1
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


def main():
    data = get_data('data/ck/Emotion/', True)
    train(data, 'model/model_ck')


main()
