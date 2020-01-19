import io
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray
import grpc
import FaceService_pb2
import FaceService_pb2_grpc
import gc
channel = grpc.insecure_channel('localhost:50001')
stub = FaceService_pb2_grpc.FaceDetectionStub(channel)

cap = cv2.VideoCapture(0)
faceDetector = MTCNN()
identityModel = tf.keras.applications.ResNet50(
        weights="./resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5",
        include_top=False,
        input_shape=(224, 224, 3),
        pooling='avg'
    )
emotionModel = tf.keras.models.load_model('./my_model.h5')
emotionList = ["Angry","Disgust","Fear","Happy","Sad","Surprise","Neutral"]

def image_to_byte_array(numpy_image):
    image = Image.fromarray(numpy_image)
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='BMP')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def getFace(image):
    results = faceDetector.detect_faces(image)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    face = image[y1:y2, x1:x2]
    return face

def getIdentity(face):
    image = cv2.resize(face, (224, 224))
    samples = asarray([asarray(image),], 'float32')
    samples = tf.keras.applications.resnet.preprocess_input(samples)
    yhat = identityModel.predict(samples).tolist()
    return yhat[0]

def getEmotion(face):
    bwface = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    bwface = cv2.resize(bwface, (48, 48))/255
	
    vg_input = np.empty([1, 48, 48, 3])
    vg_input[0][:, :, 0] = bwface
    vg_input[0][:, :, 1] = bwface
    vg_input[0][:, :, 2] = bwface
	
    emotions = emotionModel.predict(vg_input)[0]
    bestEmotion = emotions.tolist().index(max(emotions))
    return bestEmotion

while(True):
    frameData = FaceService_pb2.ImageData()
    try:
        #print("Captured Frame")
        ret, frame = cap.read()

        rawFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		
        face = getFace(rawFrame)
        frameData.ImageBytes = image_to_byte_array(face)
        #print("Extracted Face")
		
        yhat = getIdentity(face)
        frameData.embedding[:] = yhat
        #print("Generated embedding")
		
        bestEmotion = getEmotion(face)
        frameData.emotion = bestEmotion
        #print("Identified emotion")
        
        # resize pixels to the model size

    except Exception as e:
        print(e)
    finally:
        #print("Sending data")
        rsp = stub.SendProcessedData(frameData)
        gc.collect()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
