import sys
import threading
from subprocess import Popen, PIPE
from PyQt5 import QtWidgets, QtCore
import os


class OverlayWindow(QtWidgets.QWidget):
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.offset = None
        self.update_signal.connect(self.update_text)

    def init_ui(self):
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

        self.label = QtWidgets.QLabel("transcripted_text", self)
        self.label.setStyleSheet("color: white; font-size: 30px; background-color: rgba(255, 255, 0, 0);")
        self.label.adjustSize()

        self.resize(self.label.size())

    def update_text(self, new_text):
        self.label.setText(new_text)
        self.label.adjustSize()
        self.resize(self.label.size())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None


class WorkerThread(QtCore.QThread):
    def __init__(self, script_path, window):
        super().__init__()
        self.script_path = script_path
        self.window = window

    def run(self):
        process = Popen(['python', self.script_path], stdout=PIPE, stderr=PIPE, shell=True)

        def print_output():
            while True:
                output = process.stdout.readline()
                if output == b"" and process.poll() is not None:
                    break
                if output:
                    decoded_output = output.decode('utf-8').strip()
                    print(decoded_output)
                    self.window.update_signal.emit(decoded_output)

        threading.Thread(target=print_output, daemon=True).start()

        process.wait()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = OverlayWindow()
    window.show()

    script_mapping = os.path.join(os.path.dirname(__file__), "mapping.py")
    script_namename = os.path.join(os.path.dirname(__file__), "namename.py")
  #Debugging stuff done
    #printf("Debug{don't look here, there is nothing, why are you still reading?,... stop reading, bro get out, wth? why are you still reading this i'm not going to indulge, }")
    thread1 = WorkerThread(script_mapping, window)
    thread2 = WorkerThread(script_namename, window)

    thread1.start()
    thread2.start()

    sys.exit(app.exec_())
