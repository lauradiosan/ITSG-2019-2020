import sys
import uuid
import os
import glob

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import random
import functools
from detectEmotion import recognise
from VideoFrameGrabber import VideoFrameGrabber

import matplotlib.pyplot as plt

class Window2(QMainWindow):
    def __init__(self, emotions_history):
        super().__init__()

        ct = 0
        emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        media = dict(map(lambda x: (x, 0.0), emotions))

        for item in emotions_history:
            if len(item) == len(emotions):
                ct += 1
                for emotion in emotions:
                    media[emotion] += item[emotion]

        self.emotions_history = dict(map(lambda x: (x[0], x[1] / ct), media.items()))
        # print(self.emotions_history)

        self.model = QStandardItemModel(8, 2, self)
        self.model.setHeaderData(0, Qt.Horizontal, "Label")
        self.model.setHeaderData(1, Qt.Horizontal, "Quantity")

        self.pieChart = PieView()
        self.pieChart.setModel(self.model)
        
        for x in self.emotions_history.items():
            self.model.a()

        self.setCentralWidget(self.pieChart)

        self.setWindowTitle("Emotions Pie Chart")
        self.setGeometry(50, 50, 600, 600)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Kids emotion recognition'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 480
        self.pix_map = None
        self.label = None
        self.recognise_button = None
        self.file_name = ''
        self.result_label = None
        self.combo = None
        self.value_combo = 'CAFFE'
        self.input_combo = None
        self.value_input_combo = 'Image'
        self.emotions_history = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        self.mainWindow = QHBoxLayout(self)
        self.box1 = QVBoxLayout(self)
        self.box2 = QVBoxLayout(self)
        self.box2.setAlignment(Qt.AlignHCenter)
    
        self.input_combo = QComboBox()
        self.input_combo.addItem('Image')
        self.input_combo.addItem('Video')
        self.input_combo.activated[str].connect(self.onChangedInput)

        self.combo = QComboBox()
        self.combo.addItem("CAFFE")
        self.combo.addItem("FER")
        self.combo.activated[str].connect(self.onChanged)

        self.load_button = QPushButton()
        self.load_button.setText('Load')
        self.load_button.clicked.connect(self.click)

        self.recognise_button = QPushButton()
        self.recognise_button.setText('Run')
        self.recognise_button.clicked.connect(self.recognise)
        self.recognise_button.setEnabled(False)

        self.box1.addWidget(self.input_combo)
        self.input_combo.setMaximumWidth(150)
        self.input_combo.setMinimumWidth(150)
        self.box1.addWidget(self.combo)
        self.combo.setMaximumWidth(150)
        self.combo.setMinimumWidth(150)
        self.box1.addWidget(self.load_button)
        self.load_button.setMaximumWidth(150)
        self.load_button.setMinimumWidth(150)
        self.box1.addWidget(self.recognise_button)
        self.recognise_button.setMaximumWidth(150)
        self.recognise_button.setMinimumWidth(150)

        self.mainWindow.addLayout(self.box1)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setMaximumWidth(30)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setMaximumWidth(425)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.controlLayout = QHBoxLayout(self)
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton) 
        self.controlLayout.addWidget(self.positionSlider)
        self.controlLayout.setAlignment(Qt.AlignHCenter)     
        
        self.grabber = VideoFrameGrabber(self.videoWidget, self)
        self.mediaPlayer.setVideoOutput(self.grabber)
        self.grabber.frameAvailable.connect(self.process_frame)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)

        self.label = QLabel()
        self.pix_map = QPixmap()
        self.label.setPixmap(self.pix_map)
        self.label.setAlignment(Qt.AlignHCenter)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignHCenter)

        self.box2.addWidget(self.videoWidget)
        self.box2.addLayout(self.controlLayout)
        self.box2.addWidget(self.label)
        self.box2.addWidget(self.result_label)

        self.mainWindow.addLayout(self.box2)

        self.image_count = 0
        self.latest_image = None
        self.videoWidget.hide()
        self.playButton.hide()
        self.positionSlider.hide()
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawLine(170, 25, 170, 455)

    def show_chart(self):
        ct = 0
        emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        media = dict(map(lambda x: (x, 0.0), emotions))

        plot2 = []
        for item in self.emotions_history:
            if len(item) == len(emotions):
                ct += 1
                mx = ("", -1)
                for emotion in emotions:
                    if mx[1] < item[emotion]:
                        mx = (emotion, item[emotion])
                    media[emotion] += item[emotion]
                plot2 += [(ct - 1, emotions.index(mx[0]) + 1)]

        if ct == 0:
            return
        emotions_history = dict(map(lambda x: (x[0], x[1] / ct), media.items()))
        
        labels = [x for x in emotions_history.keys()]
        sizes = [x for x in emotions_history.values()]

        plt.subplot(1, 2, 1)
        patches, _ = plt.pie(sizes, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()

        plt.subplot(1, 2, 2)
        yValues = list(map(lambda x: x[1], plot2))
        plt.plot(list(map(lambda x: x[0], plot2)), yValues, 'r.-')
        plt.yticks(ticks=yValues, labels=list(map(lambda x: emotions[x - 1], yValues)))
        plt.xlabel('time (s)')
        plt.ylabel('Emotion')

        plt.tight_layout()
        plt.show()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            self.emotions_history = []

    def remove_temp_images(self):
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)

    def process_frame(self, image):
        self.latest_image = image
        self.image_count += 1

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.emotions_history = []
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.show_chart()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        # self.mediaPlayer.setVideoOutput(self.grabber)

        if self.latest_image:
            self.file_name = os.path.abspath('temp/{}.jpg'.format(str(uuid.uuid4())))
            self.latest_image.save(self.file_name)

            self.pix_map = QPixmap(self.file_name).scaled(500, 250, Qt.KeepAspectRatio)
            self.label.setPixmap(self.pix_map)
        
            # self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.recognise(None)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def click(self, e):
        options = QFileDialog.Options()
        is_image = self.value_input_combo == 'Image'
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "Choose {0}".format('image' if is_image else 'video'),
                                                   "",
                                                   "Images (*.jpg *.png *.jpeg)" if is_image else "Videos (*.avi)",
                                                   options=options)
        if file_name:
            self.recognise_button.setEnabled(True)
            self.file_name = file_name
            if is_image:
                self.pix_map = QPixmap(file_name).scaled(500, 250, Qt.KeepAspectRatio)
                self.label.setPixmap(self.pix_map)
            else:
                self.remove_temp_images()
                self.image_count = 0
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_name)))
                self.playButton.setEnabled(True)
                self.mediaPlayer.durationChanged.connect(self.durationChanged)

    def recognise(self, e):
        values = recognise(self.file_name, type=self.value_combo.lower())
        a = ""
        for (key, value) in values.items():
            a += "{0}: {1}%\n".format(key, value)
        self.emotions_history += [values]
        self.result_label.setText(a)

    def onChanged(self, text):
        self.value_combo = text

    def onChangedInput(self, text):
        self.value_input_combo = text
        if self.value_input_combo == 'Image':
            self.videoWidget.hide()
            self.playButton.hide()
            self.positionSlider.hide()
            self.recognise_button.show()
        else:
            self.videoWidget.show()
            self.playButton.show()
            self.positionSlider.show()
            self.recognise_button.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
