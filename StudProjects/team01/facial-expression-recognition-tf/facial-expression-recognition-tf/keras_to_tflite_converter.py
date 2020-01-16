"""
Converts a keras model to a tflite model.
"""
import tensorflow as tf
from tensorflow import lite

model_path = 'models/_mini_XCEPTION.110-0.68.hdf5'

converter = lite.TFLiteConverter.from_keras_model_file(model_path) 
model = converter.convert()

file = open('models/model.tflite', 'wb') 
file.write(model)

interpreter = tf.lite.Interpreter(model_path="models/model.tflite")
interpreter.allocate_tensors()

print(interpreter.get_input_details()[0]['shape'])  
print(interpreter.get_input_details()[0]['dtype']) 
print(interpreter.get_output_details()[0]['shape'])  
print(interpreter.get_output_details()[0]['dtype'])
