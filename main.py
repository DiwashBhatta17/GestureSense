import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QProgressBar, QHBoxLayout, QFrame)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from FaceRecognition import MatchTheFace as mf


def run_voice_command():
    from Backend import VoiceCommand
    VoiceCommand.main()


def run_virtual_mouse():
    import VirtualMouse as vm
    vm


class WorkerThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)

    def run(self):
        self.progress.emit(50)
        face = mf.recognize_faces()
        self.result.emit(face)
        self.progress.emit(100)


class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = WorkerThread()
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.process_result)

    def initUI(self):
        self.setWindowTitle('AI Assistant - Face Recognition')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #5a5a5a;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QProgressBar {
                text-align: center;
                border: 1px solid #5a5a5a;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 5px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_label = QLabel('AI Assistant - Face Recognition')
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.info_label = QLabel('Press the button to start face recognition')
        self.info_label.setFont(QFont('Arial', 16))
        self.info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.info_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                text-align: center;
                font-size: 16px;
                height: 25px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Start Face Recognition')
        self.start_button.clicked.connect(self.start_recognition)
        button_layout.addWidget(self.start_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def start_recognition(self):
        self.info_label.setText('Recognizing face...')
        self.progress_bar.setValue(0)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def process_result(self, face):
        if face == "yes":
            self.info_label.setText('Face recognized! Starting voice command and virtual mouse...')

            # Create threa            breakds for VoiceCommand and VirtualMouse
            voice_thread = threading.Thread(target=run_voice_command)
            virtual_mouse_thread = threading.Thread(target=run_virtual_mouse)

            # Start the threads
            voice_thread.start()
            virtual_mouse_thread.start()

        else:
            self.info_label.setText('Face not recognized. Please try again.')




def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = FaceRecognitionApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
