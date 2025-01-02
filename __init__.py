
import sys

QT6_MODE = True

if QT6_MODE:
    try:
        from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout
        from PyQt6.QtCore import Qt
        from PyQt6.QtMultimedia import QMediaDevices, QMediaCaptureSession, QCamera
        from PyQt6.QtMultimediaWidgets import QVideoWidget
        pyqt_version = "PyQt6"
    except ImportError:
        QT6_MODE = False

if not QT6_MODE:
    from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout
    from PyQt5.QtCore import Qt
    from PyQt5.QtMultimedia import QCameraInfo, QCamera as Qt5QCamera
    from PyQt5.QtMultimediaWidgets import QVideoWidget
    pyqt_version = "PyQt5"

class VideoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 300)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.available_cameras = self.get_qMediaDevices()
        if not self.available_cameras:
            return

        self.viewfinder = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.viewfinder)
        self.setLayout(layout)

        self.select_camera(0)

    def get_qMediaDevices(self):
        if pyqt_version == "PyQt6":
            return QMediaDevices.videoInputs()
        elif pyqt_version == "PyQt5":
            return QCameraInfo.availableCameras()

    def select_camera(self, i):
        if pyqt_version == "PyQt6":
            self.camera = QCamera(self.available_cameras[i])
            self.capture_session = QMediaCaptureSession()
            self.capture_session.setCamera(self.camera)
            self.capture_session.setVideoOutput(self.viewfinder)

        elif pyqt_version == "PyQt5":
            self.camera = Qt5QCamera(self.available_cameras[i])
            self.camera.setViewfinder(self.viewfinder)
            self.camera.setCaptureMode(Qt5QCamera.CaptureMode.CaptureStillImage)

        self.camera.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoWindow()
    window.show()
    sys.exit(app.exec())
else:
    window = VideoWindow()
    window.show()
