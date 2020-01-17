''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition

'''

import cv2
import os

currentPath = os.path.dirname(os.path.abspath(__file__))
face_detector = cv2.CascadeClassifier(currentPath + '/haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = 1

# Initialize individual sampling face count
count = 0

path = currentPath + '/users'
for _, _, f in os.walk(path):
    print(f)
    for file in f:
        filename = path + '/' + file
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        print(faces)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite(currentPath + '/dataset/User.' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            face_id += 1

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()


