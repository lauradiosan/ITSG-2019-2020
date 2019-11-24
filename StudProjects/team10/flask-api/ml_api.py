from flask import Flask, request
from keras.models import load_model
import tensorflow as tf
import numpy as np
import flask
from PIL import Image

app = Flask(__name__)
model = load_model('pets_classification64pixels_15epochs.h5')

# Testing url
@app.route("/hello/", methods=['GET'])
def hello():
    return "Welcome to machine learning model APIs!"

@app.route('/cnnclassifier/predict', methods=['POST', 'GET'])
def predict():
    # a = request.form['a']
    # b = request.form['b']
    img_path = 'D:/Master/Sem3/ITSG/test4.jpg'
    image = Image.open(img_path).convert('RGB')
    resized_image = image.resize((64, 64))
    resized_image = np.asarray(resized_image)
    resized_image.shape = (1, 64, 64, 3)

    # Required because of a bug in Keras when using tensorflow graph cross threads    
    result = np.argmax(model.predict(resized_image))
    data = {'result': int(result)}
    return flask.jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)