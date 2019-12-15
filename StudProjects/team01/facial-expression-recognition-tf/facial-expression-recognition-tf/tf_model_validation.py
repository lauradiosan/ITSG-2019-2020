
from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
from data_loader import *
from sklearn.metrics import classification_report, confusion_matrix


#emotion_model_path = 'models/_mini_XCEPTION.49-0.71.hdf5'
emotion_model_path = 'models/model.tflite'

model = load_model(emotion_model_path, compile=True)
#FER-2013 emotion labels: (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral)
#CK+ emotion labels:      (0=neutral, 1=anger, 2=contempt, 3=disgust, 4=fear, 5=happy, 6=sadness, 7=surprise) -> but were fixed to the FER-2013 labels
EMOTIONS = ["angry" ,"disgust", "scared", "happy", "sad", "surprised", "neutral"]

#results = model.evaluate(xtest, ytest, batch_size = 32)
#loss = model.evaluate(xtrain, ytrain, batch_size = 32, verbose = 0)
#print('test loss, test acc:', loss)

# TODO - change to test
y_pred = model.predict(faces, batch_size=64, verbose=1)
y_pred_bool = np.argmax(y_pred, axis=1)
y_rounded_train_labels = np.argmax(emotions, axis=1)

print(classification_report(y_rounded_train_labels, y_pred_bool))
cm = confusion_matrix(y_rounded_train_labels, y_pred_bool)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print(cm)