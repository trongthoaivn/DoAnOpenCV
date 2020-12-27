from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer


class frm_Loading(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Loading, self).__init__()
        uic.loadUi('Loading.ui', self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.movie = QMovie('Gif/loading.gif')
        # label
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setMovie(self.movie)
        self.timer = QTimer()
        self.movie.start()
        self.timer.singleShot(4000, self.stop)

        self.show()

    def stop(self):
        self.movie.stop()
        self.close()