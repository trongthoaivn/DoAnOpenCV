import os
import sqlite3
import sys
from datetime import datetime
import cv2
import unidecode
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import pymysql
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
from GUI.Student import frm_Student

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('D:\\DoAnOpenCV\Trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
sqliteConnection = sqlite3.connect('D:\\DoAnOpenCV\Database\db_opencv.db')
font = cv2.FONT_HERSHEY_PLAIN


class frm_Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Main, self).__init__()

        uic.loadUi('Main.ui', self)
        self.W = None
        self.frm_addStudent = None
        self.Camera = cv2.VideoCapture(0)
        self.Running = False
        self.nameStudent = None
        self.input = "(',)"
        self.output = "    "
        self.data = None
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
        self.btn_Cam_OFF.clicked.connect(self.setOff)

        # tbv_Student
        self.tbv_Student = self.findChild(QtWidgets.QTableWidget, 'tbv_Student')

        # btn_Logout
        self.btn_Logout = self.findChild(QtWidgets.QPushButton, 'btn_Logout')
        self.btn_Logout.clicked.connect(self.Logout)

        # btn_addStudent
        self.btn_addStudent = self.findChild(QtWidgets.QPushButton, 'btn_addStudent')
        self.btn_addStudent.clicked.connect(self.addStudent)

        # btn_Refresh
        self.btn_Refresh = self.findChild(QtWidgets.QPushButton, 'btn_Refresh')
        self.btn_Refresh.clicked.connect(lambda: os.system('python D:\\DoAnOpenCV/Training.py'))
        # self.btn_Refresh.clicked.connect(self.getIdStudent("1811060744"))
        # btn_Delete

        self.btn_Delete = self.findChild(QtWidgets.QPushButton, 'btn_Delete')
        self.btn_Delete.clicked.connect(self.deleteStudent)
        # txt_idStudent

        self.txt_idStudent = self.findChild(QtWidgets.QLineEdit, 'txt_idStudent')
        # self.txt_idStudent.setText("")
        # tbv_StudentAt
        self.tbv_StudentAt = self.findChild(QtWidgets.QTableWidget, 'tbv_StudentAt')

        self.show()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.timeout.connect(self.getStudentdata)
        timer.start(1000)
        self.showTime()
        self.getStudentdata()
        self.getStudentdataToAt()

    def getStudentdataToAt(self):
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM SINHVIEN"
        cursor.execute(query)
        self.data = cursor.fetchall()

    def clearTable(self):
        while self.tbv_Student.rowCount() > 0:
            self.tbv_Student.removeRow(0)

    def addStudent(self):
        self.frm_addStudent = frm_Student()

    def setOff(self):
        self.Running = True

    def deleteStudent(self):
        pass

    def attendStudent(self, Id):
        count = self.tbv_StudentAt.rowCount()
        for row in self.data:
            if row[0] == str(Id):
                print(row[0] + " " + row[1])
                self.tbv_StudentAt.insertRow(count)
                self.tbv_StudentAt.setItem(count, 0, QTableWidgetItem(row[0]))
                self.tbv_StudentAt.setItem(count, 1, QTableWidgetItem(row[1]))
                self.tbv_StudentAt.setItem(count, 2, QTableWidgetItem(row[2]))
                self.tbv_StudentAt.setItem(count, 3, QTableWidgetItem(row[3]))
                self.tbv_StudentAt.setItem(count, 4, QTableWidgetItem(row[4]))
                self.data.remove(row)

    def getIdStudent(self, Id):
        try:
            cursor = sqliteConnection.cursor()
            cursor.execute("SELECT hotenSV FROM SINHVIEN WHERE maSV='%s'" % Id)
            nameStudent = None
            for row in cursor:
                nameStudent = row
            self.nameStudent = unidecode.unidecode(nameStudent[0])

        finally:
            pass

    def Logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.hide()
            self.W = frm_Login()
        else:
            pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.setOff()
        else:
            event.ignore()

    def showTime(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.lb_Timer.setText("To Day: " + dt_string)

    def getUsername(self, name):
        self.lb_User.setText("Welcome back! " + name)

    def Cam(self):
        self.Running = False
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
                cv2.rectangle(img, (x, y), (x + w, y + h), (89, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                if (confidence < 70):
                    self.getIdStudent(id)
                    self.attendStudent(id)
                    id = self.nameStudent
                    cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (0, 255, 255), 2)
                else:
                    id = "Unknown"
                    cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (0, 25, 255), 2)

            self.displayImage(img, 1)
            cv2.waitKey()
            if self.Running:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.lb_Cam.clear()

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
            self.clearTable()
            cursor = sqliteConnection.cursor()
            cursor.execute("SELECT * FROM SINHVIEN")
            result = cursor.fetchall()
            for row_number, row_data in enumerate(result):
                self.tbv_Student.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    # print(column_number)
                    self.tbv_Student.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except pymysql.Error as e:
            print("Error")


####################################################################################################################################
class frm_Login(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Login, self).__init__()
        uic.loadUi('login_form.ui', self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.Main = None
        self.W = self
        self.button = self.findChild(QtWidgets.QPushButton, 'btn_submit')
        self.txt_US = self.findChild(QtWidgets.QLineEdit, 'txt_US')
        self.txt_PW = self.findChild(QtWidgets.QLineEdit, 'txt_PW')
        self.btn_exit = self.findChild(QtWidgets.QPushButton, 'btn_exit')
        PW = QLineEdit.Password
        self.txt_PW.setEchoMode(PW)
        self.button.clicked.connect(self.ClickButtonSubmit)
        self.btn_exit.clicked.connect(lambda: self.close())

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

            if self.W.isVisible():
                self.W.hide()
                self.Main = frm_Main()
                self.Main.getUsername(US)


app = QtWidgets.QApplication(sys.argv)
window = frm_Login()
sys.exit(app.exec_())
