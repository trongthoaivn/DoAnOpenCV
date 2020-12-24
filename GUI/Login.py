import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QLineEdit

from GUI.Main import frm_Main


class frm_Login(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Login, self).__init__()
        uic.loadUi('Login.ui', self)
        self.Main = None
        self.W = self
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

            if self.W.isVisible():
                self.W.hide()
                self.Main = frm_Main().getUsername(US)


app = QtWidgets.QApplication(sys.argv)
window = frm_Login()
sys.exit(app.exec_())
