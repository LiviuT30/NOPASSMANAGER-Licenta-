import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
import imageio
from io import BytesIO
import base64
import requests
import json
from PIL import Image

import PasswordManager

class helpLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a QLabel with the specified text
        self.text_label = QLabel("You can contact me at the email address:\nliviutomescu.work@gmail.com", self)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_label)

        # Set the layout for the QWidget
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle('Help')
        self.setFixedSize(300, 100)  # Adj

#from NewAccount import NewAccountWindow
class QRWindow(QWidget):
    def __init__(self, login_screen_instance, response):
        super().__init__()
        self.data = response
        self.login_screen = login_screen_instance
        self.initUI()

    def initUI(self):
        # Create the instruction label

        self.submit_funtion = 0

        top_layout = QHBoxLayout()
        text_layout = QVBoxLayout()
        print("HERE:",self.data)
        qr = self.data['qr_code']
        qr_code_bytes = base64.b64decode(qr)
        image = QImage.fromData(qr_code_bytes)

        self.OTP_Input = QLineEdit()
        self.OTP_Input.setPlaceholderText("Enter OTP Code")



        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(image)

        # Create a QLabel and set the pixmap
        self.QR_label = QLabel(self)
        self.QR_label.setFixedSize(150, 150)
        scaled_pixmap = pixmap.scaled(self.QR_label.size(), aspectRatioMode=1)
        self.QR_label.setPixmap(scaled_pixmap)
        self.text_label = QLabel(
            "Please scan this QR code using Google Authentificator on your phone and enter the OTP code below.",
            self
        )
        self.text_label.setWordWrap(True)

        text_layout.addWidget(self.text_label)
        text_layout.addWidget(self.OTP_Input)

        top_layout.addLayout(text_layout)
        top_layout.addWidget(self.QR_label)

        # Create the buttons
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.close_me)

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_otp)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.submit_button)

        # Set the main layout
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Verify QR')
        self.resize(400, 200)

    def submit_otp(self):
        url = 'http://127.0.0.1:5000/verify-otp'

        payload = {
            'username': self.data['username'],
            'otp': self.OTP_Input.text()
        }
        print("payload:", payload)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        if (response.status_code == 400):
            response = response.json()
            print(response['error'])
            self.text_label.setText("Invalid OTP Please Try Again")
        else:
            response = response.json()
            print(response)
            if (response['message'] == 'User created successfully'):
                print("User created successfully")

    def close_me(self):
        print("Closing window")



class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.sid_login = ''
        self.id = 0

        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(250, 250)

        self.button_login = QPushButton('Authenticate', self)
        self.button_login.clicked.connect(self.check_authenticate)
        self.button_help = QPushButton('Help!', self)
        self.button_help.setObjectName("helpButton")
        self.button_help.clicked.connect(self.open_help)

        self.button_new_account = QPushButton('New account', self)
        self.button_new_account.clicked.connect(self.show_new_account_fields)

        # Layout for the initial buttons
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button_login)
        self.button_layout.addWidget(self.button_help)
        self.button_layout.addWidget(self.button_new_account)

        # Widgets for the new account creation
        self.name_label = QLabel('Name:', self)
        self.name_input = QLineEdit(self)
        self.email_label = QLabel('Email:', self)
        self.email_input = QLineEdit(self)
        self.create_account_button = QPushButton('Create Account', self)
        self.create_account_button.clicked.connect(self.switch_to_capture_photo)

        # Layout for the new account fields (hidden initially)
        self.new_account_layout = QVBoxLayout()
        self.new_account_layout.addWidget(self.name_label)
        self.new_account_layout.addWidget(self.name_input)
        self.new_account_layout.addWidget(self.email_label)
        self.new_account_layout.addWidget(self.email_input)
        self.new_account_layout.addWidget(self.create_account_button)
        self.new_account_widget = QWidget(self)
        self.new_account_widget.setLayout(self.new_account_layout)
        self.new_account_widget.setVisible(False)

        self.facecameratext_label = QLabel(
            "Please face the camera before pressing the Submit button, a picture of you will be taken for further authentifications",
            self
        )
        self.facecameratext_label.setWordWrap(True)  # Enable word wrapping
        self.facecameratext_label.setAlignment(Qt.AlignCenter)  # Center align the text
        self.facecameratext_label.setVisible(False)  # Hidden initially

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.close_capture_photo)
        self.cancel_button.setVisible(False)  # Hidden initially

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_capture_photo)
        self.submit_button.setVisible(False)

        self.capture_photo_layout = QHBoxLayout()
        self.capture_photo_layout.addWidget(self.cancel_button)
        self.capture_photo_layout.addWidget(self.submit_button)

        # OTP input and buttons
        self.otp_label = QLabel('Enter OTP:', self)
        self.otp_input = QLineEdit(self)

        self.otp_cancel_button = QPushButton('Cancel', self)
        self.otp_cancel_button.clicked.connect(self.cancel_otp_input)

        self.otp_login_button = QPushButton('Login', self)
        self.otp_login_button.clicked.connect(self.check_authenticate_with_otp)

        # Layout for the OTP input and buttons (initially hidden)
        self.otp_layout = QVBoxLayout()
        self.otp_input_layout = QHBoxLayout()
        self.otp_input_layout.addWidget(self.otp_cancel_button)
        self.otp_input_layout.addWidget(self.otp_login_button)

        self.otp_layout.addWidget(self.otp_label)
        self.otp_layout.addWidget(self.otp_input)
        self.otp_layout.addLayout(self.otp_input_layout)
        self.otp_widget = QWidget(self)
        self.otp_widget.setLayout(self.otp_layout)
        self.otp_widget.setVisible(False)


        # Set the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.camera_label)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.new_account_widget)
        self.main_layout.addWidget(self.facecameratext_label)
        self.main_layout.addLayout(self.capture_photo_layout)
        self.main_layout.addWidget(self.otp_widget)

        self.setLayout(self.main_layout)

        # Set window properties
        self.setWindowTitle('Login')
        self.setFixedSize(270, 500)

        # Initialize the camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.cap_width = 640
        self.cap_height = 480

        # Setup a timer to update the frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(60)  # Update frame every 60 ms

    def show_otp_input(self):
        # Hide the initial buttons
        self.button_login.setVisible(False)
        self.button_help.setVisible(False)
        self.button_new_account.setVisible(False)

        # Show the OTP input and buttons
        self.otp_widget.setVisible(True)

    def cancel_otp_input(self):
        # Hide OTP input and show initial buttons
        self.otp_widget.setVisible(False)

        # Show the initial buttons
        self.button_login.setVisible(True)
        self.button_help.setVisible(True)
        self.button_new_account.setVisible(True)

    def check_authenticate_with_otp(self):
        otp_code = self.otp_input.text()
        print(f'Authenticating with OTP: {otp_code}')
        payload = {
            'otp': otp_code,
            'id': self.id
        }
        url = 'http://127.0.0.1:5000/check-otp'
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:

            response = json.loads(response.text)
            if response['message'] == 'OTP code approved, sending SID!':
                self.sid = response['sid']
                self.password_manager = PasswordManager.PasswordManagerWindow(self.sid)
                self.password_manager.show()
                self.close()
        else:
            response = json.loads(response.text)
            self.otp_label.setText('Enter OTP:\n OTP code invalid. Try again')
            print(response['error'])



    def switch_to_capture_photo(self):
        # Hide the name, email fields, and Create Account button
        self.new_account_widget.setVisible(False)

        # Show the CapturePhoto UI elements
        self.facecameratext_label.setVisible(True)
        self.cancel_button.setVisible(True)
        self.submit_button.setVisible(True)

    def close_capture_photo(self):
        print("CapturePhoto closed without submitting data to server")

        # Reset to show the account creation fields and hide the CapturePhoto elements
        self.facecameratext_label.setVisible(False)
        self.cancel_button.setVisible(False)
        self.submit_button.setVisible(False)
        self.new_account_widget.setVisible(True)

    def submit_capture_photo(self):
        photo_data = self.get_photo_as_json()
        username = self.name_input.text()
        email = self.email_input.text()
        print("Name:", username)
        print("Email:", email)
        print("Picture data:", photo_data)

        url = 'http://127.0.0.1:5000/signup'
        payload = {
            'username': username,
            'email': email,
            'image': photo_data['image']
        }
        print("payload:", payload)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Data:", response.json())
        response = response.json()
        print(response)
        if(response['message'] == 'Successful'):
            self.qr = QRWindow(self, response)
            self.qr.show()
        else:
            if(response['message'] == 'User already registered'):
                print("User already registered")

        # Hide CapturePhoto elements after submission
        #self.facecameratext_label.setVisible(False)
        #self.cancel_button.setVisible(False)
        #self.submit_button.setVisible(False)

        # Proceed with the account creation process here...
    """
    def open_picture_capture_window(self):

        self.picture_window = CapturePhoto(self)
        self.picture_window.show()

        #self.picture_window = QRWindow(self)
        #self.picture_window.show()
    """

    def show_new_account_fields(self):
        # Hide the initial buttons
        self.button_login.setVisible(False)
        self.button_help.setVisible(False)
        self.button_new_account.setVisible(False)

        # Show the new account creation fields
        self.new_account_widget.setVisible(True)

    def create_account(self):
        name = self.name_input.text()
        email = self.email_input.text()
        # Here, you would add logic to handle creating a new account.
        print(f'Creating account for {name} with email {email}')
        # After account creation, you might want to reset the form or close the window.

    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the image to Qt format
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(250, 250, Qt.KeepAspectRatio)
            self.camera_label.setPixmap(QPixmap.fromImage(p))

    def get_photo_as_json(self):
        try:
            ret, frame = self.cap.read()
            frame = frame[:, 80:560, :]
            frame = cv2.resize(frame, (105, 105))
            retval, buffer = cv2.imencode('.jpg', frame)
            cv2.imwrite('test.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            data = {'image': jpg_as_text}
            return data
        except Exception as e:
            print("Exception occurred: ", e)

    def check_authenticate(self):
        try:
            data = self.get_photo_as_json()
            print(data)
            url = 'http://127.0.0.1:5000/authentificate'

            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, json=data, headers=headers)

            response = json.loads(response.text)
            if response['message'] == 'Data received successfully!':
                id = response['id']
                if id != 0:
                    print("login successful - id: ", id)
                    self.id = id
                    self.show_otp_input()
            else:
                print(response['message'])


        except Exception as e:
            print("Exception occurred: ", e)

    def open_password_manager(self):
        self.password_manager_window = PasswordManager.PasswordManagerWindow(self.sid_login)
        self.password_manager_window.show()
        self.close()

    def open_help(self):
        self.help = helpLoginWindow()
        self.help.show()
        print('opening help')

    def closeEvent(self, event):
        self.cap.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    login = LoginScreen()
    login.show()

    sys.exit(app.exec_())
