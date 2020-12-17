import sys
import threading
import time
from datetime import datetime
from timeit import Timer

from IPython.external.qt_for_kernel import QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation, QTimer
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from js2py.base import false, true


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
