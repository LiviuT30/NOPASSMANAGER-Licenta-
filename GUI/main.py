import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QLineEdit
from PyQt5.QtGui import QPixmap
import imageio
from io import BytesIO
import base64
import requests
import json
from PIL import Image

#from NewAccount import NewAccountWindow
class NewAccountWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Initialize the camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.cap_width = 640
        self.cap_height = 480

        # Setup a timer to update the frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update frame every 20 ms

    def initUI(self):
        # Create widgets
        self.text_label = QLabel(self)
        self.text_label.setText(
            "Create a new account by filling in your details."
        )
        self.text_label.setWordWrap(True)

        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(250, 250)

        self.name_label = QLabel('Name:', self)
        self.name_input = QLineEdit(self)

        self.email_label = QLabel('Email:', self)
        self.email_input = QLineEdit(self)

        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.create_account_button = QPushButton('Create Account', self)
        self.create_account_button.clicked.connect(self.create_account)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('New Account')
        self.resize(300, 500)

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

    def create_account(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        # Here, you would add logic to handle creating a new account.
        print(f'Creating account for {name} with email {email}')
        # After account creation, you might want to close this window and reopen the login window.
        self.close()

    def closeEvent(self, event):
        self.cap.release()


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(250, 250)

        self.button_login = QPushButton('Authenticate', self)
        self.button_help = QPushButton('Help!', self)
        self.button_help.setObjectName("helpButton")


        self.button_naccount = QPushButton('New account', self)
        self.button_naccount.clicked.connect(self.new_account)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.camera_label)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_help)
        layout.addWidget(self.button_naccount)

        self.button_login.clicked.connect(self.check_authenticate)
        self.button_help.clicked.connect(self.open_help)

        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Login')
        self.setFixedSize(270, 400)

        # Initialize the camera

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.cap_width = 640
        self.cap_height = 480

        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        # Setup a timer to update the frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update frame every 20 ms
    def new_account(self):
        self.new_account_window = NewAccountWindow()
        self.new_account_window.show()
        self.close()
###################################

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

    def check_authenticate(self):
        try:

            ret, frame = self.cap.read()
            # ratio 640 - 480 = 160 / 2 = 80
            print(frame.shape)
            frame = frame[:,80:560,:]
            frame = cv2.resize(frame, (105,105))
            retval, buffer = cv2.imencode('.jpg', frame)
            cv2.imwrite('test.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            print(jpg_as_text)


            #DECODE FROM BASE64 TO ARRAY

            #jpg_original = base64.b64decode(jpg_as_text)
            #jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            #image_buffer = cv2.imdecode(jpg_as_np, flags=1)

            #print(image_buffer.shape)


            data = {'img': jpg_as_text}
            url = 'http://127.0.0.1:5000/authentificate'

            headers = {'Content-Type': 'application/json'}

            # Send the POST request with the JSON data
            response = requests.post(url, json=data, headers=headers)

            # Return the response from the server
            print(response.json())
            response = json.loads(response.text)
            #TO CHANGE
            if response['message'] == 'Data received successfully!':
                sid = response['sid']
                print(sid)

        except Exception as e:
            print("Exception occured: ", e)

    def open_pm(self):
        print("TODO")





    def open_help(self):
        self.help = helpLoginWindow()
        self.help.show()
        print('todo')

    def closeEvent(self, event):
        self.cap.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    login = LoginScreen()
    login.show()


    sys.exit(app.exec_())