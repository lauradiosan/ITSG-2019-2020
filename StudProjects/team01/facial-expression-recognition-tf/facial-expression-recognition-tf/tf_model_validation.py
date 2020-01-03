"""
Validates the model against the (faces, emotions) from a dataset,
read through the data_loader module, printing the precision for each label,
as well as the confusion matrix for the model.
"""
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import load_model
import numpy as np
from data_loader import faces, emotions

emotion_model_path = 'models/_mini_XCEPTION.110-0.68.hdf5'

model = load_model(emotion_model_path, compile=True)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

y_pred = model.predict(faces, batch_size=64, verbose=1)
y_pred_bool = np.argmax(y_pred, axis=1)
y_rounded_train_labels = np.argmax(emotions, axis=1)

print(classification_report(y_rounded_train_labels, y_pred_bool))
cm = confusion_matrix(y_rounded_train_labels, y_pred_bool)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print(cm)
