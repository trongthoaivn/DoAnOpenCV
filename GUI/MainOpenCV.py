import sys
from datetime import datetime

import cv2
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation, QTimer
from PyQt5.QtWidgets import QMessageBox, QLineEdit


class frm_Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Main, self).__init__()
        uic.loadUi('Main.ui', self)
        self.W = self
        self.page_list = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')

        # btn_Home

        self.btn_Home = self.findChild(QtWidgets.QPushButton, 'btn_Home')
        self.page_Home = self.findChild(QtWidgets.QWidget, 'Home')
        self.btn_Home.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Home))

        # btn_Lecturer

        self.btn_Lecturer = self.findChild(QtWidgets.QPushButton, 'btn_Lecturer')
        self.page_Lecturer = self.findChild(QtWidgets.QWidget, 'Lecturer')
        self.btn_Lecturer.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Lecturer))

        # btn_Subject

        self.btn_Subject = self.findChild(QtWidgets.QPushButton, 'btn_Subject')
        self.page_Subject = self.findChild(QtWidgets.QWidget, 'Subject')
        self.btn_Subject.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Subject))

        # btn_Lesson

        self.btn_Lession = self.findChild(QtWidgets.QPushButton, 'btn_Lession')
        self.page_Lession = self.findChild(QtWidgets.QWidget, 'Lession')
        self.btn_Lession.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Lession))

        # btn_Account

        self.btn_Account = self.findChild(QtWidgets.QPushButton, 'btn_Account')
        self.page_Account = self.findChild(QtWidgets.QWidget, 'Account')
        self.btn_Account.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Account))
        # btn_Help

        self.btn_Help = self.findChild(QtWidgets.QPushButton, 'btn_Help')
        self.page_Help = self.findChild(QtWidgets.QWidget, 'Help')
        self.btn_Help.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Help))

        # btn_Class

        self.btn_Class = self.findChild(QtWidgets.QPushButton, 'btn_Class')
        self.page_Class = self.findChild(QtWidgets.QWidget, 'Class')
        self.btn_Class.clicked.connect(lambda: self.page_list.setCurrentWidget(self.page_Class))

        # lb_Timer

        self.lb_Timer = self.findChild(QtWidgets.QLabel, 'lb_Timer')

        # lb_User
        self.lb_User = self.findChild(QtWidgets.QLabel, 'lb_User')

        # lb_Cam
        self.lb_Cam = self.findChild(QtWidgets.QLabel, 'lb_cam')
        # self.lb_Cam.setPixmap()

        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

    def showTime(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.lb_Timer.setText("To Day: " + dt_string)

    def getUsername(self, name):
        self.lb_User.setText("Welcome back! " + name)

    def cam(self):
        faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
        eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
        smileCascade = cv2.CascadeClassifier('Cascades/haarcascade_smile.xml')

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)  # set Width
        cap.set(4, 480)  # set Height

        while True:
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y: y + h, x: x + w]
                roi_color = img[y: y + h, x: x + w]

                eyes = eyeCascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.5,
                    minNeighbors=5,
                    minSize=(5, 5),
                )

                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                smile = smileCascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.5,
                    minNeighbors=15,
                    minSize=(25, 25),
                )

                for (xx, yy, ww, hh) in smile:
                    cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)

                cv2.imshow('video', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:  # press 'ESC' to quit
                break

        cap.release()
        cv2.destroyAllWindows()


class frm_Login(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Login, self).__init__()
        uic.loadUi('Login.ui', self)

        self.Main = self
        self.button = self.findChild(QtWidgets.QPushButton, 'btn_submit')
        self.txt_US = self.findChild(QtWidgets.QLineEdit, 'txt_US')
        self.txt_PW = self.findChild(QtWidgets.QLineEdit, 'txt_PW')
        PW = QLineEdit.Password
        self.txt_PW.setEchoMode(PW)
        self.button.clicked.connect(self.ClickButtonSubmit)

        self.show()

    def ClickButtonSubmit(self):
        msb = QMessageBox()
        US = self.txt_US.text()
        PW = self.txt_PW.text()
        if US != "admin" or PW != "123":
            msb.setWindowTitle("Warning!")
            msb.setText("Login fail! please try again.")
            msb.exec_()
        else:

            if self.Main.isVisible():
                self.Main.hide()
                self.Main = frm_Main()
                self.Main.getUsername(US)
                self.Main.show()


app = QtWidgets.QApplication(sys.argv)
window = frm_Login()
app.exec_()
