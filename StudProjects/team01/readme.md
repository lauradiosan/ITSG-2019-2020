# Intelligent Tools for Social Good
 ITSG app and research for 2019-2020
 Contains for now:
  - report (app description, problem definition, related work, useful tools, experimentation methodology and results)
  - intelligent algorithm (model training/testing and running)
  - acting mirror app (recognizes facial expression of people based on a video stream from the camera/file/youtube)

# Acting Mirror Mind-Map and User Manual
 The Acting Mirror app takes a video stream from the camera, from a file on the machine it runs on, or from a youtube video, and processes the video stream drawing rectangles around the face of people in the stream and labeling them with one of 7 emotions: "angry", "disgust", "scared", "happy", "sad", "surprised", "neutral".

 As illustrated before, the app works by reading a video stream, and passing that stream to a the haarscade frontal face detector. For each detected face, an intelligent alogirthm parses the pixels of the face in the format of a 48x48 grayscale pixel matrix, and labels the face with one of 7 emotions. In the end, the processed output video stream is shown to the user and also saved in a file called "output.avi".
 ![Acting Mirror Mind-Map](https://i.imgur.com/4cWIonj.png)
 
 Prerequisites for the app:
 - Python 3.x
 - Tensorflow installed, preferably the tensorflow-gpu. (we use version 1.15.0-rc2)
 - Have the following python modules installed in your environemnt: keras, imutils, cv2, numpy, matplotlib, pafy
 
 The app is written in python, so it can be run on any desktop OS, and starting the app is done with the following command:
```
python acting_mirror.py
```
 There are a number of settings available to customize the acting mirror session using the following options for the above command:
```
optional arguments:
  -h, --help            show this help message and exit
  --camera CAMERA       camera from which to stream, referenced by its
                        identifier
  --video VIDEO         offline video source from which to stream and to
                        display the emotions
  --youtube URL         youtube video source from which to stream and to
                        display the emotions
  --details             flag to show the emotion details window, if missing,
                        the emotion detials window will not show
  --graph               flag to show a graph with the emotions percentage over
                        time, if missing, the graph will not show
  --disable_rectangles  flag to disable showing the face rectangles on the
                        acting mirror window, if missing, the face rectangles
                        will show
```
 For example, running the following command:
```
python acting_mirror.py --youtube https://www.youtube.com/watch?v=pqTntG1RXSY --details --graph
```
 would yield the following result (video from the series Silicon Valley, the episode with the Hotdog, Not Hotdog app):
 ![Hotdog, Not Hotdog App](https://i.imgur.com/qA8uhM4.png)
 Using the commands **--camera**, **--video** and **--youtube** in the same time, does not result in error. They are simply taken into account in the following order of precedence: first is **--camera**, then **--video** and last, but not least **--youtube**.
 
 Not using the options for **--details** and for **--graph** results in just the main window showing up.
 
 Closing the session is done pressing the key **q**.
 
 Once the session is closed, it is saved in the **output.avi** file.
 
 Improvements that can be made:
 - allow changing the intelligent model through arguments (maybe add support for both keras models and tflite models)
 - use a better model, the current one has an overall accuracy of 65%
 - optimize the model or the data flow for videos (the current model is trained with pictures, not videos)

 Here is a mind-map proposing 5 different applications for the FER problem in pursuit of social good:
 ![MindMap](https://i.imgur.com/IG7xmbs.png)
