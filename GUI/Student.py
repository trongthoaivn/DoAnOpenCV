import os
import sqlite3
import sys
import time
import cv2
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox

from GUI.Loading import frm_Loading

CURR_DIR = os.path.dirname(__file__)
faceCascade = cv2.CascadeClassifier('%s/Cascades/haarcascade_frontalface_default.xml' % CURR_DIR)
sqliteConnection = sqlite3.connect('%s/Database/db_opencv.db' % CURR_DIR[0:13])


class frm_Student(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Student, self).__init__()
        self.OffCam = False  # set camera is on
        self.Save = False  # set Save  image is No
        self.Detect = True
        self.Id = None

        uic.loadUi('%s/Student.ui' % CURR_DIR, self)

        # lb_Cam

        self.lb_Cam = self.findChild(QtWidgets.QLabel, 'lb_Cam')

        # btn_Save

        self.btn_Save = self.findChild(QtWidgets.QPushButton, 'btn_Save')
        self.btn_Save.clicked.connect(self.insertOrUpdate)

        # btn_Detect

        self.btn_Detect = self.findChild(QtWidgets.QPushButton, 'btn_Detect')
        self.btn_Detect.clicked.connect(self.setDetect)

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
        # Display camera
        self.capTrue()

    def clearText(self):
        # clear text on textbox after insert Student
        self.txt_ID.clear()
        self.txt_Name.clear()
        self.txt_Class.clear()
        self.txt_Birth.clear()

    def setDetect(self):
        if self.Detect:
            self.Detect = False
        else:
            self.Detect = True

    def setOff(self):
        # turn off camera
        self.OffCam = True

    def SaveImg(self, Id):
        # save image
        self.Save = True
        self.Id = Id

    def closeEvent(self, event):
        # confirm close window
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.setOff()
            sqliteConnection.close()
        else:
            event.ignore()

    def insertOrUpdate(self):
        # insert Student
        # get student information
        Id = self.txt_ID.text()
        Name = self.txt_Name.text()
        Birth = self.txt_Birth.text()
        Class = self.txt_Class.text()
        if self.rdb_Male.isChecked():
            Sex = "Nam"
        else:
            Sex = "Nữ"
        # find Student in Database: if exist is update record else insert new record
        if (self.txt_ID.text() != "") and (self.txt_Name.text() != ""):
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
            # capture image
            self.setDetect()
            time.sleep(2)
            self.SaveImg(Id)
            # confirm Save
            time.sleep(1)
            msb = QMessageBox()
            msb.setIcon(QMessageBox.Information)
            msb.setText("Save student information successfully!")
            msb.setWindowTitle("Notification")
            msb.exec_()
            # clear textbox
            self.clearText()

    def capTrue(self):
        cap = cv2.VideoCapture(0)
        self.OffCam = False
        while cap.isOpened():

            ret, img = cap.read()
            # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # detect face
            if self.Detect:
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(20, 20)
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            elif self.Save:
                if os.path.exists("%s/Dataset/%s.png" % (CURR_DIR[0:13], self.Id)):
                    os.remove("%s/Dataset/%s.png" % (CURR_DIR[0:13], self.Id))
                cv2.imwrite("%s/Dataset/%s.png" % (CURR_DIR[0:13], self.Id), img)
                self.Save = False
                self.Detect = True

            # display image to label
            self.displayImage(img)
            cv2.waitKey()
            # turn off camera or save image
            if self.OffCam:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.lb_Cam.clear()

    def displayImage(self, img):
        # image to label pixmap
        Qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                Qformat = QImage.Format_RGBA888
            else:
                Qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], Qformat)
        img = img.rgbSwapped()
        self.lb_Cam.setPixmap(QPixmap.fromImage(img))

#
# app = QtWidgets.QApplication(sys.argv)
# window = frm_Student()
# sys.exit(app.exec_())
