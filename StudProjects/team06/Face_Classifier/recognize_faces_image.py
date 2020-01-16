import base64
import pickle

import cv2
import face_recognition
import numpy as np
from flask import Flask, request
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def index():
	try:
		imgData = request.data
		imgData = base64.b64decode(imgData)
		img = np.asarray(bytearray(imgData), dtype="uint8")
		img = cv2.imdecode(img, cv2.IMREAD_COLOR)
		rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		image = imutils.resize(img, width=800)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		rects = detector(gray, 2)

		if len(rects)>1:
			return "Too many faces"
		faceAligned = fa.align(image, gray, rects[0])

		# detect the (x, y)-coordinates of the bounding boxes corresponding
		# to each face in the input image, then compute the facial embeddings
		# for each face
		print("[INFO] recognizing faces...")
		boxes = face_recognition.face_locations(faceAligned)
		encodings = face_recognition.face_encodings(faceAligned, boxes)

		if(len(encodings)>1):
			return "Too many faces"

		# initialize the list of names for each face detected
		names = []

		matches = face_recognition.compare_faces(data["encodings"],
													 encodings[0])
		name = "Unknown"

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
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number of
			# votes (note: in the event of an unlikely tie Python will
			# select first entry in the dictionary)
			name = max(counts, key=counts.get)
		return name
	except:
		return "Some error occured"

if __name__ == '__main__':
	data = pickle.loads(open("encodingAligned.pickle", "rb").read())
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	fa = FaceAligner(predictor, desiredFaceWidth=256)
	app.run(host='0.0.0.0', debug=True)
