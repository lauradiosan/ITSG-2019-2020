from flask import Flask, request
from keras.models import load_model
import tensorflow as tf
import numpy as np
import pandas as pd
import flask
from PIL import Image
from sklearn.externals import joblib

app = Flask(__name__)

cnn = load_model('pets_classification64pixels_15epochs.h5')
clf = joblib.load('pets_mlp.pkl')

@app.route('/cnnclassifier/predict', methods=['POST'])
def predict():
	# run CNN Prediction
    img_path = request.json['imgPath']
    img_path = 'D:/Master/Sem3/ITSG/' + img_path
    image = Image.open(img_path).convert('RGB')
    resized_image = image.resize((64, 64))
    resized_image = np.asarray(resized_image)
    resized_image.shape = (1, 64, 64, 3)

    # Required because of a bug in Keras when using tensorflow graph cross threads    
    pred_cnn = np.argmax(cnn.predict(resized_image))

    # run MLP Prediction
    data = request.json
    if 'imgPath' in data: 
    	del data['imgPath']

	# the clf model takes 55 parameters (55 pet features)
    clf_in = np.zeros((55))
    i = 0
    for col in data:
    	clf_in[i] = data[col]
    	i += 1
    
    pred_mlp = clf.predict([clf_in])

    # combine the model results
    prediction = int((pred_cnn+pred_mlp)/2)
    data = {'result': prediction}
    return flask.jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)