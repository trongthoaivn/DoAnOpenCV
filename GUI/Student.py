import sqlite3
import cv2
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
sqliteConnection = sqlite3.connect('D:\\DoAnOpenCV\Database/db_opencv.db')


class frm_Student(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Student, self).__init__()
        self.Running = False
        uic.loadUi('Student.ui', self)

        # lb_Cam
        self.lb_Cam = self.findChild(QtWidgets.QLabel, 'lb_Cam')
        # btn_Save
        self.btn_Save = self.findChild(QtWidgets.QPushButton, 'btn_Save')
        self.btn_Save.clicked.connect(self.insertOrUpdate)
        # txt_ID
        self.txt_ID = self.findChild(QtWidgets.QLineEdit, 'txt_ID')
        # txt_Name
        self.txt_Name = self.findChild(QtWidgets.QLineEdit, 'txt_Name')
        # txt_Birth
        self.txt_Birth = self.findChild(QtWidgets.QLineEdit, 'txt_Birth')
        # txt_Class
        self.txt_Class = self.findChild(QtWidgets.QLineEdit, 'txt_Class')
        # rdb_Male
        self.rdb_Male = self.findChild(QtWidgets.QRadioButton, 'rdb_Male')
        # rdb_Female
        self.rdb_Female = self.findChild(QtWidgets.QRadioButton, 'rdb_Female')
        self.show()

    def clearText(self):
        self.txt_ID.clear()
        self.txt_Name.clear()
        self.txt_Class.clear()
        self.txt_Birth.clear()

    def setOff(self):
        self.Running = True

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.setOff()
            sqliteConnection.close()
        else:
            event.ignore()

    def insertOrUpdate(self):
        Id = self.txt_ID.text()
        Name = self.txt_Name.text()
        Birth = self.txt_Birth.text()
        Class = self.txt_Class.text()
        if self.rdb_Male.isChecked():
            Sex = "Nam"
        else:
            Sex = "Nữ"
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM sinhvien WHERE maSV ='%s'" % Id
        cursor.execute(query)
        isRecordExist = 0
        for row in cursor:
            isRecordExist = 1
        if isRecordExist == 0:
            query = "insert into sinhvien  values('%s','%s','%s','%s','%s')" % (Id, Name, Birth, Sex, Class)

        else:
            query = "update  sinhvien set maSV='%s', hotenSV ='%s', ngaysinhSV ='%s', gioitinhSV ='%s', lopSV='%s' " \
                    "where maSV='%s'" % (
                        Id, Name, Birth, Sex, Class, Id)

        cursor.execute(query)
        sqliteConnection.commit()
        self.capTrue()
        self.clearText()

    def capTrue(self):
        self.Running = False
        Id = self.txt_ID.text()
        count = 0
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
                count += 1
                cv2.imwrite("D:\\DoAnOpenCV\Dataset/Student." + str(Id) + '.' + str(count) + ".jpg",
                            gray[y:y + h, x:x + w])
            self.displayImage(img, 1)
            cv2.waitKey()
            if self.Running:
                break
            elif count >= 100:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.lb_Cam.clear()
        msb = QMessageBox()
        msb.setIcon(QMessageBox.Information)
        msb.setText("Save student information successfully!")
        msb.setWindowTitle("Notification")
        msb.exec_()

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


# app = QtWidgets.QApplication(sys.argv)
# window = frm_Student()
# sys.exit(app.exec_())
