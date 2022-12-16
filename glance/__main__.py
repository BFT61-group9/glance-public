"""
GLANCE - DEMO VERSION
"""
__version__ = "0.36.0"
import os
import sys
import datetime

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit
from PyQt5.QtGui import QImage, QPixmap
import face_recognition
import numpy as np
import cv2

import resource
from app_util import here_location, location_wrap as locw, make_dir
from maintenance import load_data, load_data_new
from payment import momo_pay
from user import validate_username, User, export_to_json

make_dir("UserDB") # Init database
asset_path = os.path.join(here_location(), "asset")
userdb_path = locw("UserDB")

MAIN_UI = "mainwindow2.ui"
OUTPUT_UI = "outputwindow3.ui"
MAKEACC_UI = "accwindow.ui"


# Main window
class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi(os.path.join(asset_path, MAIN_UI), self)

        self.runButton.clicked.connect(self.runSlot)
        self.makeAccButton.clicked.connect(self.makeAccSlot)

        self._new_window = None
        self.Videocapture_ = None

    def refreshAll(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.Videocapture_ = "0"

    @pyqtSlot()
    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        ui.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")
    
    @pyqtSlot()
    def makeAccSlot(self):
        """
        Called when the user presses the Create Account button
        """
        print("Clicked Create Account")
        self.refreshAll()
        print(self.Videocapture_)
        ui.hide()  # hide the main window
        self.createAccountWindow()  # Create and open new output window
    
    def createAccountWindow(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_CreateAccountDialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")



# Make Account Window
class Ui_CreateAccountDialog(QDialog):
    def __init__(self):
        super(Ui_CreateAccountDialog, self).__init__()
        loadUi(os.path.join(asset_path, MAKEACC_UI), self)

        #Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        self.image = None
        self.users_list = [dir for dir in os.listdir(userdb_path) if os.path.isdir(os.path.join(userdb_path, dir))]

    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        else:
            self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms
    

    def update_frame(self):
        _, self.image = self.capture.read()
        self.displayImage(self.image, 1)

    def displayImage(self, image, window=1):
        """
        :param image: frame from camera
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
        
        # Capture
        if self.MakeAccButton.isChecked():
            self.MakeAccButton.setChecked(False)
            flag1 = False
            flag2 = False
            print("Working")
            
            input_username = self.usernameEdit.text()
            input_fname = self.fnameEdit.text()
            input_lname = self.lnameEdit.text()
            
            if input_username == "" or input_fname == "" or input_lname == "":
                self.StatusLabel.setText("Must fill all the fields")
            else:
                flag1 = True
            
            if input_username in self.users_list:
                self.StatusLabel.setText("Username already exist!")
            else:
                if validate_username(input_username):
                    flag2 = True
                else:
                    self.StatusLabel.setText("Username must only include [a-zA-Z0-9]")
            
            # self.StatusLabel.setText(f"{flag1}, {flag2}") # Check all conditions
            if flag1 and flag2: # all conditions met
                user = User(input_username, input_fname, input_lname)
                user.update_balance(500000) # Demo
                userpath = make_dir(userdb_path, input_username)
                export_to_json(user.export(), os.path.join(userpath, f"{input_username}.json"))

                print("Capturing image...")
                img_path = os.path.join(userpath, f"{input_username}.jpg")
                cv2.imwrite(img_path, self.image)
                print("Image captured!")

                print("Encoding image...")
                print(f"Load image from {img_path}")
                loaded_img = face_recognition.load_image_file(img_path)
                encoded_img = face_recognition.face_encodings(loaded_img)[0]
                np.save(os.path.join(userpath, f"{input_username}.npy"), encoded_img)
                print("Image encoded!")

                self.StatusLabel.setText("Account created")



# Output Window
class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi(os.path.join(asset_path, OUTPUT_UI), self)

        #Update time
        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)

        self.image = None

    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        else:
            self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        
        data = load_data_new(userdb_path)

        self.name_list = [(dat[1], dat[2]) for dat in data]
        self.encode_list = [dat[0] for dat in data]
        self.TimeList1 = []
        self.TimeList2 = []

        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, name_list):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param name_list: known face names
        :return:
        """

        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            
            if match[best_match_index]:
                udat = name_list[best_match_index][1] # User data
                self.UsernameLabel.setText(udat["username"])
                self.FullnameLabel.setText(f"{udat['fname']} {udat['lname']}")
                self.BalanceLabel.setText(f"{udat['balance']:,}")

                def quick_pay(amount:int, udat=udat):
                    bal = udat["balance"]
                    if bal < amount:
                        self.StatusLabel.setText("Insufficient Balance")
                    else:
                        new_bal = bal - amount
                        try:
                            momo_pay(amount)
                        except:
                            pass
                        else:
                            udat["balance"] = new_bal
                            self.StatusLabel.setText("Success")
                
                if self.PayButton.isChecked():
                    self.PayButton.setChecked(False)
                    pay_amount = int(self.lineEdit.text())
                    quick_pay(pay_amount)
                
                
                name = name_list[best_match_index][0].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        return frame


    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.name_list, 1)

    def displayImage(self, image, encode_list, name_list, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param name_list: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, name_list)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)


# Output
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
