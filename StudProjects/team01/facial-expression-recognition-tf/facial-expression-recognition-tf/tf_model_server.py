
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import tensorflow as tf
from PIL import Image

# parameters for loading data and images
detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
#emotion_model_path = 'models/_mini_XCEPTION.97-0.65.hdf5'
emotion_model_path = 'models/model.tflite'

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
#emotion_classifier = load_model(emotion_model_path, compile=False)
interpreter = tf.lite.Interpreter(model_path=emotion_model_path)
interpreter.allocate_tensors()
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

def classify_picture(image_pixels, width, height):
    #should read a frame from picture
    img = Image.new('L', (width, height), "black")
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i,j] = image_pixels[i][j] # Set the colour accordingly    
    #img.show()
    open_cv_image = numpy.array(img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    
    frame = open_cv_image
    #frame = camera.read()[1]
    #reading the frame
    frame = imutils.resize(frame,width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    
    if len(faces) > 0:
        faces = sorted(faces, reverse=True,
        key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
                    # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
            # the ROI for classification via the CNN
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        
        
        #preds = emotion_classifier.predict(roi)[0]
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], roi)
        interpreter.invoke()
        preds = interpreter.get_tensor(output_details[0]['index'])[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]

        emotions_text = []
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            # construct the label text
            text = "{}: {:.2f}%".format(emotion, prob * 100)
            emotion_text.add(text)
            w = int(prob * 300)
        print(emotion_text)

from flask import Flask, request
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class EmotionController(Resource):
    def post(self):
        json_body = request.get_json()
        json_body = str(json_body)
        #json_body = json_body.replace('\t', '').replace('\n', '').replace(',}', '}').replace(',]',']').replace('\'', '"')
        json_body = json_body.replace('\'', '"')
        body = json.loads(json_body)
        return {'you sent': body['message']}, 201
    def get(self):
        return {'message': 'Hi'}
        
api.add_resource(EmotionController, '/emotion')

if __name__ == '__main__':
    app.run(debug=True)