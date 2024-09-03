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
class NewAccountWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create widgets
        self.text_label = QLabel(self)
        self.text_label.setText(
            "Create a new account by filling in your details."
        )
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
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
        self.resize(300, 200)

    def create_account(self):
        name = self.name_input.text()
        email = self.email_input.text()
        # Here, you would add logic to handle creating a new account.
        print(f'Creating account for {name} with email {email}')
        # After account creation, you might want to close this window and reopen the login window.
        self.close()