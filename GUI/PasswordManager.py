import sys
import cv2
import numpy as np
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QSize
from PyQt5.QtGui import QImage, QMouseEvent, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QCheckBox, QScrollArea, QTextEdit, QLineEdit
from PyQt5.QtGui import QPixmap
import imageio
from io import BytesIO
import base64
import requests
import json
from PIL import Image

from AddPassword import addPasswordWindow, generate_random_password
from ModifyPassword import modifyPasswordWindow

class PasswordWidget(QWidget):
    def __init__(self, sid, parent=None):
        super().__init__(parent)
        self.sid = sid
        self.initUI()


    def initUI(self):

        window_height = 600
        window_width = 1000

        self.id = 0
        self.framepass = QFrame(self)
        self.width = (window_width / 4) * 3
        self.height = (window_height / 11)
        self.framepass.setFixedWidth(int(self.width)-70)
        self.framepass.setFixedHeight(int(self.height))
        #self.setStyleSheet("background-color: {}; border: 2px solid black".format("#f0f0f0"))
        self.layout = QHBoxLayout()

        self.edit_button = QPushButton(self)
        self.edit_button.setIcon(QIcon('edit.png'))  # Replace with your image path
        self.edit_button.setIconSize(QSize(30, 40))  # Adjust the size as needed
        self.edit_button.setFlat(True)
        self.edit_button.clicked.connect(self.edit_clicked)

        self.setLayout(self.layout)

        self.textedits = []
        for _ in range(2):
            textEdit = QTextEdit(self)
            textEdit.setReadOnly(True)
            #textEdit.setStyleSheet("border: 0.5px solid black; border-radius: 2px")
            textEdit.setFixedHeight(int(self.height / 2))
            self.layout.addWidget(textEdit)
            self.textedits.append(textEdit)

        self.enterdate = QLabel(self)
        self.enterdate.setFixedWidth(180)
        self.enterdate.setFixedHeight(40)
        self.layout.addWidget(self.enterdate)
        self.checkbox = QCheckBox(self)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.edit_button)



    def set_password(self, password):
            self.textedits[0].setText(password)
            if password == '':
                self.textedits[0].setStyleSheet("border: 0px solid black; border-radius: 2px")
                self.textedits[0].setFixedHeight(0)
            else:
                self.textedits[0].setFixedHeight(35)
                self.textedits[0].setStyleSheet("border: 1px solid black; border-radius: 2px")
    def set_name(self, name):
            self.textedits[1].setText(name)
            if name == '':
                self.textedits[1].setStyleSheet("border: 0px solid black; border-radius: 2px")
                self.textedits[1].setFixedHeight(0)
            else:
                self.textedits[1].setFixedHeight(35)
                self.textedits[1].setStyleSheet("border: 1px solid black; border-radius: 2px")


    def set_date(self, date):
            self.enterdate.setText(date)

    def set_id(self, id):
            self.id = id

    def check_checkbox(self):
            if self.checkbox.isChecked():
                return "checked"
            else:
                return "unchecked"
    def uncheck_checkbox(self):
        if self.checkbox.isChecked():
            self.checkbox.setChecked(False)

    def setH_check_and_edit(self, h):
        self.checkbox.setFixedHeight(h)
        self.edit_button.setFixedHeight(h)


    def set_color(self, color):
        self.setStyleSheet("background-color: {};".format(color))
        self.framepass.setStyleSheet("background-color: {}; border: 0px solid Black;".format(color))


    def edit_clicked(self):
            # Only react to left mouse button clicks
            print(self.textedits[1].toPlainText())
            self.modifywindow = modifyPasswordWindow(sid= self.sid, id= self.id, name= self.textedits[1].toPlainText(), password= self.textedits[0].toPlainText())
            self.modifywindow.show()





class button_menu(QWidget):
    delete_passwords_signal = pyqtSignal()
    nextpage_signal = pyqtSignal()
    previouspage_signal = pyqtSignal()
    get_passwords_signal = pyqtSignal()


    def __init__(self, sid, parent=None):
        super().__init__(parent)
        self.sid = sid
        self.initUI()


    def initUI(self):

        window_height = 600
        window_width = 1000

        self.width = (window_width / 4) * 1

        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: #f0f0f0; border: 3px solid black; border-radius: 8px;")



        self.frame.setFixedSize(int(self.width), window_height-50)

        self.addpass = QPushButton('Add a password', self)
        self.addpass.clicked.connect(self.open_add_password_window)

        self.getpass = QPushButton('Get Passwords', self)
        self.getpass.clicked.connect(self.get_passwords_signal.emit)

        self.nextpage = QPushButton('Next', self)
        self.nextpage.clicked.connect(self.nextpage_signal.emit)

        self.lastpage = QPushButton('Previous', self)
        self.lastpage.clicked.connect(self.previouspage_signal.emit)

        self.deletepass = QPushButton('Delete Checked', self)
        self.deletepass.clicked.connect(self.delete_passwords_signal.emit)

        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.getpass)
        self.layout.addWidget(self.nextpage)
        self.layout.addWidget(self.lastpage)
        self.layout.addWidget(self.deletepass)
        self.layout.addWidget(self.addpass)


        self.setLayout(self.layout)
        #self.setStyleSheet("background-color: Yellow;")

        self.setFixedSize(int(self.width), window_height-50)

    def open_add_password_window(self):
        # Create an instance of AddPasswordWindow
        self.add_password_window = addPasswordWindow(self.sid)
        self.add_password_window.show()

class password_menu(QWidget):

    def __init__(self, sid, parent=None):
        super().__init__(parent)
        self.sid = sid
        self.initUI()


    def initUI(self):

        window_height = 600
        window_width = 1000

        self.passwords = np.array([])
        self.names = np.array([])
        self.dates = np.array([])

        self.press_get_passwords_true = 0


        self

        self.width = (window_width / 4) * 3
        self.frame = QFrame(self)
        self.widget = QWidget()

        self.frame.setStyleSheet("background-color: white; border: 3px solid Black; border-radius: 8px;")
        self.frame.setFixedSize(int(self.width)-50, window_height - 50)
        #self.frame.setFixedWidth(int(self.width)-50)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        #self.setStyleSheet("background-color: Green;")
        self.width = (window_width / 4) * 3
        self.setFixedSize(int(self.width)-50, window_height-50)
        #self.setFixedWidth(int(self.width) - 50)

    def add_password_widget(self, password, name, date, color,pass_id):
        # MODIFY
        password_widget = PasswordWidget(sid = self.sid)
        password_widget.set_password(password)

        password_widget.set_color(color)
        password_widget.set_name(name)
        password_widget.set_date(date)
        password_widget.set_id(pass_id)
        if pass_id == 0:
            password_widget.setH_check_and_edit(0)
        else:
            password_widget.setH_check_and_edit(40)
        self.layout.addWidget(password_widget)

    def get_passwords(self):

        url = 'http://127.0.0.1:5000/getpasswords'
        payload = {
            'sid': self.sid
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Data:", response.json())
        response = response.json()

        self.passwords = []
        self.names = []
        self.dates = []
        self.passwords_id = []
        # Extract the data from the response
        if response['passwords'] == 'Passwords not found':
                print("Passwords not found")
        else:
            for entry in response['passwords']:
                self.passwords_id.append(entry['id'])
                self.passwords.append(entry['password'])
                self.names.append(entry['name'])
                self.dates.append(entry['date_modified'])



        self.clear_layout()
        self.press_get_passwords_true = 1
        for idx, magic in enumerate(self.passwords):
            print(magic)
            print('here')
            color = "#f0f0f0" if idx % 2 == 0 else "#4CAF50"
            self.add_password_widget(self.passwords[idx], self.names[idx], self.dates[idx], color, self.passwords_id[idx])
            if idx == 9:
                break
        z = 10 - len(self.passwords)
        if z > 0:
            if z % 2 == 0:
                for i in range(10 - len(self.passwords)):
                    color = "#f0f0f0" if i % 2 == 0 else "#4CAF50"
                    self.add_password_widget('', '', '', color, 0)
            else:
                for i in range(10 - len(self.passwords)):
                    color = "#4CAF50" if i % 2 == 0 else "#f0f0f0"
                    self.add_password_widget('', '', '', color, 0)

        '''passwords = []
        names = []
        dates = []
        self.clear_layout()
        print(self.sid)
        self.press_get_passwords_true = 1
        for idx, magic in enumerate(passwords):
            print(magic)
            color = "#f0f0f0" if idx % 2 == 0 else "#4CAF50"
            self.add_password_widget(passwords[idx],names[idx], dates[idx], color)
            if idx == 9:
                break'''


    def uncheck_checkboxes(self):
        # Iterate over all child widgets in the layout
        arr = np.array([])
        current_page = self.press_get_passwords_true

        for i in range(self.layout.count()):
            placeholder = self.layout.itemAt(i).widget()
            xd = placeholder.check_checkbox()
            placeholder.xd = placeholder.uncheck_checkbox()
            arr = np.append(arr, xd)

        print(arr)
        return arr

    def delete_checked(self):

        arr = self.uncheck_checkboxes()
        idx_arr = np.array([])

        for idx, txt in enumerate(arr):
            if txt == 'checked':
                idx_arr = np.append(idx_arr, int(self.passwords_id[idx]))
        idx_arr = idx_arr.astype(int)
        print(idx_arr)
        url = 'http://127.0.0.1:5000/deletepassword'
        payload = {
            'sid': self.sid,
            'password_ids': idx_arr.tolist()
            
        }
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Data:", response.json())
        self.get_passwords()



    def clear_layout(self):
       while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def next_page(self):

        current_page = self.press_get_passwords_true
        number_of_passwords = len(self.passwords)
        if number_of_passwords <= current_page*10:
            print("No more passwords to load")
        else:
            if current_page:
                print(current_page)
                for x in range(0,10):

                   idx =  x + (10*current_page)
                   placeholder = self.layout.itemAt(x)

                   if placeholder and placeholder.widget():
                       placeholder = placeholder.widget()

                   if(idx < number_of_passwords):
                       #element = "pass{}".format(idx+1)

                       placeholder.set_password(self.passwords[idx])
                       placeholder.set_name(self.names[idx])
                       placeholder.set_date(self.dates[idx])
                       placeholder.set_id(self.passwords_id[idx])
                       placeholder.setH_check_and_edit(40)

                   else:
                       placeholder.set_password("")
                       placeholder.set_name("")
                       placeholder.set_date("")
                       placeholder.set_id(0)
                       placeholder.setH_check_and_edit(0)


                self.press_get_passwords_true = current_page + 1

            else:
                print('You need to press the Get Passwords button first')
        print("NextButton Pressed")

    def reload_page(self):

        current_page = self.press_get_passwords_true
        number_of_passwords = len(self.passwords)

        if current_page > 0:
            print(current_page)
            for x in range(0, 10):

                idx = x + (10 * (current_page - 1))
                placeholder = self.layout.itemAt(x)

                if placeholder and placeholder.widget():
                    placeholder = placeholder.widget()

                if (idx < number_of_passwords):
                    # element = "pass{}".format(idx + 1)

                    placeholder.set_password(self.passwords[idx])
                    placeholder.set_name(self.names[idx])
                    placeholder.set_date(self.dates[idx])
                    placeholder.set_id(self.passwords_id[idx])
                    placeholder.setH_check_and_edit(40)

                else:
                    placeholder.set_password("")
                    placeholder.set_name("")
                    placeholder.set_date("")
                    placeholder.set_id(0)
                    placeholder.setH_check_and_edit(0)

        else:
            print('You are on the first page or you didnt press the Get Passwords button')
    def previous_page(self):
        current_page = self.press_get_passwords_true
        number_of_passwords = len(self.passwords)

        if current_page > 1:
            print(current_page)
            for x in range(0, 10):

                idx = x + (10 * (current_page - 2))
                placeholder = self.layout.itemAt(x)

                if placeholder and placeholder.widget():
                    placeholder = placeholder.widget()

                if (idx < number_of_passwords):
                    #element = "pass{}".format(idx + 1)

                    placeholder.set_password(self.passwords[idx])
                    placeholder.set_name(self.names[idx])
                    placeholder.set_date(self.dates[idx])
                    placeholder.set_id(self.passwords_id[idx])
                    placeholder.setH_check_and_edit(40)

                else:
                    placeholder.set_password("")
                    placeholder.set_name("")
                    placeholder.set_date("")
                    placeholder.set_id(0)
                    placeholder.setH_check_and_edit(0)
            self.press_get_passwords_true = current_page - 1
        else:
            print('You are on the first page or you didnt press the Get Passwords button')


class PasswordManagerWindow(QWidget):
    def __init__(self, sid, parent=None):
        super().__init__(parent)
        self.sid = sid
        self.initUI()

    def initUI(self):

        window_height = 600
        window_width = 1000

        self.layout = QHBoxLayout()

        self.button_menu = button_menu(sid= self.sid)
        self.password_menu = password_menu(sid= self.sid)
        #self.scroll = QScrollArea()
        #self.scroll.setWidget(self.password_menu)

        self.layout.addWidget(self.button_menu)
        self.layout.addWidget(self.password_menu)

        self.setLayout(self.layout)
        self.setFixedSize(window_width, window_height)
        #self.setStyleSheet("background-color: #f0f0f0;")
        self.button_menu.delete_passwords_signal.connect(self.password_menu.delete_checked)
        self.button_menu.nextpage_signal.connect(self.password_menu.next_page)
        self.button_menu.previouspage_signal.connect(self.password_menu.previous_page)
        self.button_menu.get_passwords_signal.connect(self.password_menu.get_passwords)

        self.setWindowTitle('NoPassManager')


#fa parolele in clientside stelute