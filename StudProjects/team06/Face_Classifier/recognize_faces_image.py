import base64
import pickle

import cv2
import face_recognition
import numpy as np
from flask import Flask, request

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def index():
	try:
		imgData = request.data
		imgData = base64.b64decode(imgData)
		img = np.asarray(bytearray(imgData), dtype="uint8")
		img = cv2.imdecode(img, cv2.IMREAD_COLOR)
		rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes corresponding
		# to each face in the input image, then compute the facial embeddings
		# for each face
		print("[INFO] recognizing faces...")
		boxes = face_recognition.face_locations(rgb)
		encodings = face_recognition.face_encodings(rgb, boxes)

		if (len(encodings) > 1):
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
	data = pickle.loads(open("encodings1.pickle", "rb").read())
	app.run(host='0.0.0.0', debug=True)
