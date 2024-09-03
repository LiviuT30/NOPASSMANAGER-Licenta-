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
import random
import string

def generate_random_password(length=12):
    # Define the character sets
    letters = string.ascii_letters  # Includes both lowercase and uppercase letters
    digits = string.digits          # Includes digits 0-9
    special_chars = string.punctuation  # Includes special characters like !, @, #

    # Combine all the character sets
    all_chars = letters + digits + special_chars

    # Ensure the password has at least one letter, one digit, and one special character
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars)
    ]

    # Fill the rest of the password length with random characters
    password += random.choices(all_chars, k=length-3)

    # Shuffle the result to avoid predictable patterns
    random.shuffle(password)

    # Convert the list to a string
    return ''.join(password)




class modifyPasswordWindow(QWidget):
    def __init__(self, sid, id, name, password ,parent=None):
        super().__init__(parent)
        self.sid = sid
        self.password_id = id
        self.name = name
        self.password = password
        self.initUI()

    def initUI(self):
        # Create widgets
        self.name_label = QLabel("Name:")
        self.name_text = QLineEdit(self)
        self.name_text.setText(self.name)
        self.password_label = QLabel("Password:")
        self.password_text = QLineEdit(self)
        self.password_text.setText(self.password)

        self.buttons_layout = QHBoxLayout()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.modify_password)

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.insert_password)

        self.cancel_button = QPushButton("Cancel")

        self.buttons_layout.addWidget(self.submit_button)
        self.buttons_layout.addWidget(self.generate_button)
        self.buttons_layout.addWidget(self.cancel_button)

        #Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_text)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_text)
        layout.addLayout(self.buttons_layout)



        self.setLayout(layout)
        # Set window properties

        self.setWindowTitle('Modify Password')
        self.resize(300, 200)

    def modify_password(self):

        url = 'http://127.0.0.1:5000/modifypassword'
        payload = {
            'sid': self.sid,
            'password_id': self.password_id,
            'password': self.password_text.text(),
            'name': self.name_text.text()
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

        self.close()

    def insert_password(self):
        x = generate_random_password()
        self.password_text.setText(x)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    login = modifyPasswordWindow()
    login.show()
    sys.exit(app.exec_())