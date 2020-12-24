import sys
from datetime import datetime
import cv2
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import pymysql
from PyQt5.QtWidgets import QTableWidgetItem

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')


class frm_Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Main, self).__init__()
        self.db = pymysql.connect("localhost", "root", "1234", "db_opencv")
        uic.loadUi('Main.ui', self)
        self.W = self
        self.Camera = cv2.VideoCapture(0)
        self.Running = False
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

        # btn_Cam
        self.btn_Cam = self.findChild(QtWidgets.QPushButton, 'btn_Cam')
        self.btn_Cam.clicked.connect(self.Cam)
        # btn_Cam_OFF
        self.btn_Cam_OFF = self.findChild(QtWidgets.QPushButton, 'btn_Cam_OFF')
        #self.btn_Cam_OFF.clicked.connect(self.x)
        # tbv_Student
        self.tbv_Student = self.findChild(QtWidgets.QTableWidget, 'tbv_Student')

        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        self.getStudentdata()

    def x(self):
        self.Running = True

    def showTime(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.lb_Timer.setText("To Day: " + dt_string)

    def getUsername(self, name):
        self.lb_User.setText("Welcome back! " + name)

    def Cam(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
            self.displayImage(img, 1)
            cv2.waitKey()
            if self.Running:
                break

        cap.release()

    def displayImage(self, img, window=1):
        Qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                Qformat = QImage.Format_RGBA888
            else:
                Qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], Qformat)
        img = img.rgbSwapped()
        self.lb_Cam.setPixmap(QPixmap.fromImage(img))

    def getStudentdata(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM sinhvien")
            result = cursor.fetchall()
            self.tbv_Student.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tbv_Student.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    # print(column_number)
                    self.tbv_Student.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except pymysql.Error as e:
            print("Error")
