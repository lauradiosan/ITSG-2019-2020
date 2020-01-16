# import the necessary packages
from facealigner import FaceAligner
from imutils import paths
import face_recognition
import pickle
import os
# import the necessary packages
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2



# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images("datasetkids"))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
fa = FaceAligner(predictor, desiredFaceWidth=256)

print("Nr. of images trained:%d".format(len(imagePaths)))
# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    if imagePath.split(os.path.sep)[-2] == "test":
        continue
    # extract the person name from the image path
    print("[INFO] processing image {}/{}".format(i + 1,
                                                 len(imagePaths)))
    name = imagePath.split(os.path.sep)[-3]

    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    try:
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=800)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 2)
    except:
        continue

    for rect in rects:
        # extract the ROI of the *original* face, then align the face
        # using facial landmarks
        (x, y, w, h) = rect_to_bb(rect)
        try:
            faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
            faceAligned = fa.align(image, gray, rect)
        except:
            continue
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(faceAligned)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("alignedKids.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
