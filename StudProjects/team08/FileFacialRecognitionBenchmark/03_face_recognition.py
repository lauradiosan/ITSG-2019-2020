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
smileCascade = cv2.CascadeClassifier(currentPath + '/Cascades/haarcascade_smile.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

names = ['None']
# names related to ids: example ==> Marcelo: id=1,  etc
for i in range(1,13234): #14000
	names.append('User'+str(i))

# Initialize and start realtime video capture
# cam = cv2.VideoCapture(0)
# cam.set(3, 640) # set video widht
# cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 10.0
minH = 10.0

avgSmile = 0
avgSmileDetected = 0
smileNotDetected = 0

path = currentPath + '/dataset'
for _, _, f in os.walk(path):
    for file in f:
		filename = path + '/' + file
		img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
		faces = faceCascade.detectMultiScale(
			img,
			scaleFactor = 1.2,
			minNeighbors = 5,
			minSize = (int(minW), int(minH)),
		   )
		
		if(not any(map(len, faces))):
			smileNotDetected = smileNotDetected + 1;
		
		for(x,y,w,h) in faces:
			id, confidence = recognizer.predict(img[y:y+h,x:x+w])
			# Check if confidence is less them 100 ==> "0" is perfect match
			if (confidence < 100):
			
				smile = smileCascade.detectMultiScale(
					img,
					scaleFactor= 1.5,
					minNeighbors=15,
					minSize=(int(minW), int(minH)),
					)
				
				if(smile is not None):
					listId = names[id]
					listConfidence = "{0}%".format(round(100 - confidence))
					avgSmile = avgSmile + round(100 - confidence);
					avgSmileDetected = avgSmileDetected + 1;
					print("Perfect match. Confidence: " + listConfidence + " " + listId + ". Smile detected!")
					
			else:
				id = "unknown"
				confidence = "  {0}%".format(round(100 - confidence))
				print("Unknown face")
				
if(not avgSmileDetected == 0):
	print('Avg smile detection: {0}'.format(avgSmile/avgSmileDetected))
	
print('Smile not detected: {0}'.format(smileNotDetected))

cv2.destroyAllWindows()
