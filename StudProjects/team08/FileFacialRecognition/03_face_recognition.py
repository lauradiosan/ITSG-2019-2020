"""
Real Time Face Recogition
==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc
==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition
"""

import cv2
import numpy as np
import os
from PIL import Image
import sys

currentPath = os.path.dirname(os.path.abspath(__file__))
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(currentPath + '/trainer/trainer.yml')
haarCascadePath = currentPath + '/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(haarCascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'User1', 'User2', 'User3', 'User4', 'User5', 'User6', 'User7', 'User8', 'User9', 'User10']

# Initialize and start realtime video capture
# cam = cv2.VideoCapture(0)
# cam.set(3, 640) # set video widht
# cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 48.0
minH = 64.0

file = sys.argv[1];

path = currentPath + '/../ClientApp/src/assets/icons'

# path = currentPath + '/dataset'
for _, _, f in os.walk(path):
    # for file in f:
	filename = path + '/' + file
	img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	faces = faceCascade.detectMultiScale(
		img,
		scaleFactor = 1.2,
		minNeighbors = 5,
		minSize = (int(minW), int(minH)),
	   )
	for(x,y,w,h) in faces:
		cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
		id, confidence = recognizer.predict(img[y:y+h,x:x+w])
		# Check if confidence is less them 100 ==> "0" is perfect match
		if (confidence < 100):
			id = names[id]
			confidence = "{0}%".format(round(100 - confidence))
			print("Perfect match. Confidence: " + confidence + " " + id)
		else:
			id = "unknown"
			confidence = "  {0}%".format(round(100 - confidence))
			print("Unknown face")

cv2.destroyAllWindows()
