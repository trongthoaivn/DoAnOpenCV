import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar

class QTimer_ProgressBar(QMainWindow):

    def __init__(self):
        super().__init__()

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 70,400, 50)
        self.pbar.setValue(0)

        self.setWindowTitle("QTimer Progressbar")
        self.setGeometry(64,64,640,480)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(100)

    def handleTimer(self):
        value = self.pbar.value()
        if value < 100:
            value = value + 1
            self.pbar.setValue(value)
        else:
            self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QTimer_ProgressBar()
    sys.exit(app.exec_())