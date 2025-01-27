
import sys
from queue import Queue

from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QComboBox,
                            QGraphicsView, QGraphicsScene, QStatusBar, QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt, QCameraPermission
from PyQt6.QtMultimedia import QMediaDevices, QMediaCaptureSession, QCamera, QImageCapture
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem

image_queue = Queue(maxsize=100)

class VideoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint| Qt.WindowType.Dialog)
        self.resize(300, 300)

        self.available_cameras = QMediaDevices.videoInputs()
        if not self.available_cameras:
            return

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.graphics_scene = QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.graphics_scene)
        self.video_item = QGraphicsVideoItem()
        self.graphics_scene.addItem(self.video_item)

        layout = QVBoxLayout()
        layout.addWidget(self.graphics_view)

        self.setup_ui(layout)
        self.setLayout(layout)
        self.select_camera(0)

        self.show()

    def setup_ui(self, layout:QVBoxLayout):
        self.status_bar = QStatusBar(self)
        self.status_bar.setFixedHeight(20)
        layout.addWidget(self.status_bar)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.capture_button = QPushButton("capture", self)
        button_layout.addWidget(self.capture_button)

        camera_selector = QComboBox()
        camera_selector.setStatusTip("Choose camera")
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)
        camera_selector.addItems([camera.description() for camera in self.available_cameras])
        camera_selector.currentIndexChanged.connect(self.select_camera)

        button_layout.addWidget(camera_selector)

        button_layout.addStretch()

    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setVideoOutput(self.video_item)

        self.image_capture = QImageCapture(self.camera)
        self.capture_session.setImageCapture(self.image_capture)
        self.capture_button.clicked.connect(self.image_capture.capture)

        self.image_capture.imageCaptured.connect(self.on_image_captured)

        self.camera.start()
        self.current_camera_name = self.available_cameras[i].description()

    @pyqtSlot(int, QImage)
    def on_image_captured(self, id, image: QImage):
        if not image_queue.empty():
            image_queue.get()
        image_queue.put(image)
        print(image)

def checkCameraPermission(permission=None):
    camera_permission = QCameraPermission()
    permission = app.checkPermission(camera_permission)
    if permission == Qt.PermissionStatus.Granted:
        print("Camera permission is granted! :-)")
        run_video()
    else:
        print("Camera permission is Not granted :-(")

video_window = None
def run_video():
    global video_window
    video_window = VideoWindow()
    video_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
else:
    from aqt import mw
    app = mw.app

camera_permission = QCameraPermission()
permission_status = app.checkPermission(camera_permission)
if permission_status == Qt.PermissionStatus.Undetermined:
    app.requestPermission(camera_permission, checkCameraPermission)
else:
    checkCameraPermission(permission_status)

if __name__ == "__main__":
    sys.exit(app.exec())

