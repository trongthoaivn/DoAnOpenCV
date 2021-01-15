import csv
import os
import sqlite3
import sys
from datetime import datetime
import cv2
import face_recognition
import unidecode
import numpy as np
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt
import xlwt

from GUI.Student import frm_Student

CURR_DIR = os.path.dirname(__file__)
sqliteConnection = sqlite3.connect('%s/Database/db_opencv.db' % CURR_DIR[0:13])
font = cv2.FONT_HERSHEY_PLAIN


class frm_Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Main, self).__init__()

        uic.loadUi('%s/Main.ui' % CURR_DIR, self)
        self.W = None
        self.frm_addStudent = None
        self.Camera = cv2.VideoCapture(0)
        self.Running = False
        self.Count = 0
        self.nameStudent = None
        self.input = "(',)"
        self.output = "    "
        self.data = None
        self.process_this_frame = True
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
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
        self.tbv_Student.cellClicked.connect(self.GetIdtoDelete)

        # btn_Logout
        self.btn_Logout = self.findChild(QtWidgets.QPushButton, 'btn_Logout')
        self.btn_Logout.clicked.connect(self.Logout)

        # btn_addStudent

        self.btn_addStudent = self.findChild(QtWidgets.QPushButton, 'btn_addStudent')
        self.btn_addStudent.clicked.connect(self.addStudent)

        # btn_Refresh

        self.btn_Refresh = self.findChild(QtWidgets.QPushButton, 'btn_Refresh')
        self.btn_Refresh.clicked.connect(lambda: os.system('python.exe %s/Trainer/Training.py' % CURR_DIR[0:13]))

        # btn_Export

        self.btn_Export = self.findChild(QtWidgets.QPushButton, 'btn_Export')
        self.btn_Export.clicked.connect(self.exportData)

        # btn_Delete

        self.btn_Delete = self.findChild(QtWidgets.QPushButton, 'btn_Delete')
        self.btn_Delete.clicked.connect(self.deleteStudent)

        # txt_Count

        self.txt_Count = self.findChild(QtWidgets.QTextBrowser, 'txt_Count')

        # txt_idStudent

        self.txt_idStudent = self.findChild(QtWidgets.QLineEdit, 'txt_IDStudent')

        # tbv_StudentAt

        self.tbv_StudentAt = self.findChild(QtWidgets.QTableWidget, 'tbv_StudentAt')

        # RunSlot:
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

    def deleteStudentinDb(self, ID):
        cursor = sqliteConnection.cursor()
        query = "DELETE FROM SINHVIEN WHERE maSV ='%s'" % ID
        cursor.execute(query)
        sqliteConnection.commit()

    def delteStudentinFile(self, ID):
        if os.path.exists("%s/Dataset/%s.png" % (CURR_DIR[0:13], ID)):
            os.remove("%s/Dataset/%s.png" % (CURR_DIR[0:13], ID))

    def clearAtTable(self):
        while self.tbv_StudentAt.rowCount() > 0:
            self.tbv_StudentAt.removeRow(0)

    def clearTable(self):
        while self.tbv_Student.rowCount() > 0:
            self.tbv_Student.removeRow(0)

    def addStudent(self):

        self.frm_addStudent = frm_Student()

    def setOff(self):
        self.Running = True

    def GetIdtoDelete(self):
        row = self.tbv_Student.currentRow()
        idRow = self.tbv_Student.item(row, 0).text()
        self.txt_idStudent.setText(idRow)

    def deleteStudent(self):
        if self.txt_idStudent.text() != "":
            reply = QMessageBox.question(self, 'Delete',
                                         'Are you sure you want to delete student %s?' % self.txt_idStudent.text(),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.deleteStudentinDb(self.txt_idStudent.text())
                self.delteStudentinFile(self.txt_idStudent.text())
                self.txt_idStudent.clear()
            else:
                pass
        else:
            reply = QMessageBox.question(self, 'None selected student',
                                         'Please select the student to delete', QMessageBox.Ok)

    def exportData(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.tbv_StudentAt.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, QtCore.Qt.Horizontal)
            sheet.write(0, c + 1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, QtCore.Qt.Vertical)
            sheet.write(r + 1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r + 1, c + 1, text)
        wbk.save(filename)

    def attendStudent(self, Id):
        count = self.tbv_StudentAt.rowCount()
        for row in self.data:
            if row[0] == str(Id):
                self.Count += 1
                self.txt_Count.setText(str(self.Count))
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print(row[0] + " " + row[1])
                self.tbv_StudentAt.insertRow(count)
                self.tbv_StudentAt.setItem(count, 0, QTableWidgetItem(row[0]))
                self.tbv_StudentAt.setItem(count, 1, QTableWidgetItem(row[1]))
                self.tbv_StudentAt.setItem(count, 2, QTableWidgetItem(dt_string))
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
            self.setOff()
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
        with open('%s/Trainer/data.csv' % CURR_DIR[0:13], 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                text = row[1].replace("]", "").replace("[", "")
                array_face = np.fromstring(text, dtype=float, sep='  ')
                self.known_face_encodings.append(array_face)
                self.known_face_names.append(row[0])

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 441)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 901)
        while cap.isOpened():
            # Grab a single frame of video
            ret, frame = cap.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if self.process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[int(best_match_index)]

                    self.face_names.append(name)

            self.process_this_frame = not self.process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (89, 255, 0), 2)

                # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                self.getIdStudent(name)
                self.attendStudent(name)
                cv2.putText(frame, self.nameStudent, (left - 50, top - 5), font, 1.0, (0, 255, 255), 1)

            self.displayImage(frame, 1)
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
        except sqlite3.Error as e:
            print("Error")


########################################################################################################################
class frm_Login(QtWidgets.QMainWindow):

    def __init__(self):
        super(frm_Login, self).__init__()
        uic.loadUi('%s/login_form.ui' % CURR_DIR, self)
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
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT taiKhoan , matKhau , hotenGV FROM GIANGVIEN ")
        result = cursor.fetchall()
        for row in result:
            if US != row[0] or PW != row[1]:
                msb.setWindowTitle("Warning!")
                msb.setText("Login fail! please try again.")
                msb.exec_()
            else:
                if self.W.isVisible():
                    self.W.hide()
                    self.Main = frm_Main()
                    self.Main.getUsername(row[2])

#
#
# app = QtWidgets.QApplication(sys.argv)
# window = frm_Main()
# sys.exit(app.exec_())
