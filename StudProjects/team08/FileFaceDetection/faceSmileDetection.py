import cv2
import numpy as np
import os
from PIL import Image
import sys


# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
currentPath = os.path.dirname(os.path.abspath(__file__))
faceCascade = cv2.CascadeClassifier(currentPath + '/Cascades/haarcascade_frontalface_default.xml')
smileCascade = cv2.CascadeClassifier(currentPath + '/Cascades/haarcascade_smile.xml')

minW = 48.0
minH = 64.0
file = sys.argv[1];

path = currentPath + '/../ClientApp/src/assets/icons'

for _, _, f in os.walk(path):
	filename = path + '/' + file
	gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,      
        minSize=(30, 30)
	)

	for (x,y,w,h) in faces:
		cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		
		smile = smileCascade.detectMultiScale(
			roi_gray,
			scaleFactor= 1.5,
			minNeighbors=15,
			minSize=(25, 25),
			)
		
		for (xx, yy, ww, hh) in smile:
			print('smile detected')


cv2.destroyAllWindows()
