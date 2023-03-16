"""
https://www.geeksforgeeks.org/creating-a-camera-application-using-pyqt5/
"""
import os
import sys
import time
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import QMainWindow, QErrorMessage, QApplication, QLabel, QWidget, QVBoxLayout
from dotenv import find_dotenv, load_dotenv

from utils import upload_file_to_drive, send_picture, open_messenger


load_dotenv(find_dotenv())


SEND_TO_MESSENGER = False
SEND_TO_DRIVE = True


class MainWindow(QMainWindow):

    # Setting up

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background : black;")
        if SEND_TO_MESSENGER:
            self.firefox = open_messenger()

        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            print("No camera found")
            sys.exit()
        self.save_path = "./pictures/"
        Path(self.save_path).mkdir(parents=True, exist_ok=True)

        self.setup_main_widget()
        self.setWindowTitle("Picbooth")
        self.showMaximized()
        self.show()
        self.is_taking_picture = False

    def setup_main_widget(self):
        # Camera viewfinder
        self.video = QCameraViewfinder(self)
        self.video.show()
        self.select_camera(0)

        # Label
        self.label = QLabel("", self)
        self.label.setFont(QFont("Verdana", 40, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.label.setStyleSheet("color: white;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video)
        layout.addWidget(self.label)
        self.main_widget = QWidget()
        self.main_widget.setLayout(layout)
        self.setCentralWidget(self.main_widget)

        self.is_taking_picture = False

    def select_camera(self, i):
        print(self.available_cameras[i])
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.video)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda error_msg, error, msg: self.alert(msg))

    # Taking a Picture

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.is_taking_picture:
            self.is_taking_picture = True
            self.countdown = 3
            self.run_countdown()
        event.accept()

    def run_countdown(self):
        print("i = ", self.countdown)
        if self.countdown == 0:
            self.timer.stop()
            self.label.setText("")
            self.set_and_clear_white_screen(500)
            self.timer.singleShot(200, self.take_picture)
        if self.countdown == 3:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.run_countdown)
            self.timer.start(1000)
        self.label.setText(str(self.countdown))
        self.countdown -= 1

    def take_picture(self):
        print("Taking picture")
        timestamp = time.strftime("%d-%m-%Y-%H_%M_%S")
        picture_path = os.path.join(self.save_path, f"picbooth-{timestamp}.jpg")
        self.capture.capture(os.path.join(picture_path))
        print("Saved picture: ", picture_path)
        if SEND_TO_DRIVE:
            self.send_picture_to_gdrive(picture_path)
        if SEND_TO_MESSENGER:
            self.send_picture_to_messenger(picture_path)

    def set_and_clear_white_screen(self, duration):
        self.set_white_screen()
        timer = QTimer(self)
        timer.singleShot(duration, self.setup_main_widget)

    def set_white_screen(self):
        white_widget = QWidget(self)
        white_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(white_widget)

    def send_picture_to_gdrive(self, picture_path):
        timer = QTimer(self)
        timer.singleShot(4000, lambda: upload_file_to_drive(picture_path))

    def send_picture_to_messenger(self, picture_path):
        timer = QTimer(self)
        timer.singleShot(4000, lambda: send_picture(os.path.abspath(picture_path), self.firefox))

    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec())
