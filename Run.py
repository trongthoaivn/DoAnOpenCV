import sys

from PyQt5.QtWidgets import QApplication

from GUI.Main import frm_Login

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = frm_Login()
    sys.exit(app.exec_())