import face_recognition
import cv2
import pickle
from imutils import paths
import os
import shutil

data = pickle.loads(open("encodingUnalignedBenchmarkHog.pickle", "rb").read())

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
print("[INFO] recognizing faces...")

cnt = 0
trues = 0
falses = 0
imagePaths = list(paths.list_images("dataset/lfw_home/lfw_funneled"))
for (i, imagePath) in enumerate(imagePaths):
    if imagePath.split(os.path.sep)[-2] == "train":
        continue

    cnt+=1

    name = imagePath.split(os.path.sep)[-3]

    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb,model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)

    print(cnt)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        guess = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                guess = data["names"][i]
                counts[guess] = counts.get(guess, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            guess = max(counts, key=counts.get)

        # update the list of names
        names.append(guess)
    if len(names) > 1:
        cnt-=1
        shutil.rmtree(os.path.abspath("dataset/lfw_home/lfw_funneled/"+name))
        print("Too many faces.Image:{0} name:{1}".format(cnt,name))
        continue
    if len(names) == 0:
        cnt-=1
        continue
    print("{0}->{1}".format(name,names[0]))
    if names[0] == name:
        trues+=1
    else:
        falses+=1

print("Nr of test images:{0}".format(cnt))
print("Trues:{0}".format(trues))
print("Accuracy:{0}".format((trues * 100)/cnt))