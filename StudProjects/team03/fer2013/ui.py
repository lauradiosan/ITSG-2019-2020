import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
import random
import functools
from detectEmotion import recognise


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Kids emotion recognition'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.pix_map = None
        self.label = None
        self.recognise_button = None
        self.file_name = ''
        self.result_label = None
        self.combo = None
        self.value_combo = 'CAFFE'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        layout = QVBoxLayout(self)

        self.label = QLabel()
        self.pix_map = QPixmap()
        self.label.setPixmap(self.pix_map)

        button = QPushButton()
        button.setText('Load Image')
        button.clicked.connect(self.click)

        self.recognise_button = QPushButton()
        self.recognise_button.setText('Recognise Emotions')
        self.recognise_button.clicked.connect(self.recognise)
        self.recognise_button.setEnabled(False)

        self.result_label = QLabel()
        self.combo = QComboBox()
        self.combo.addItem("CAFFE")
        self.combo.addItem("FER")
        self.combo.activated[str].connect(self.onChanged) 

        layout.addWidget(button)
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.recognise_button)
        layout.addWidget(self.result_label)
        self.show()

    def click(self, e):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "Choose photo",
                                                   "D:\\AI\\Datasets\\databrary-30\\databrary30-LoBue-Thrasher-The Child_Affective_Facial\\sessions",
                                                   "Images (*.jpg *.png *.jpeg)",
                                                   options=options)
        if file_name:
            self.recognise_button.setEnabled(True)
            self.file_name = file_name
            self.pix_map = QPixmap(file_name).scaled(500, 250, Qt.KeepAspectRatio)
            self.label.setPixmap(self.pix_map)

    def recognise(self, e):
        values = recognise(self.file_name, type=self.value_combo.lower())
        a = ""
        for (key, value) in values.items():
            a += "{0}: {1}%\n".format(key, value)
        self.result_label.setText(a)

    def onChanged(self, text):
        self.value_combo = text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
