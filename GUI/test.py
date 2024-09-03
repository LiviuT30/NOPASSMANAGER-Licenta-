def get_passwords(self, passwords):
    self.clear_layout()
    Array_passwords = np.array([])
    for idx, password in enumerate(passwords):

        pass_wrap = QFrame(self)
        pass_wrap.setStyleSheet("background-color: #4CAF50; border: 2px solid black; border-radius: 8px;")
        # pass_wrap.setFixedSize(int(self.width)-80, int((window_height - 50) / 10))

        pass_layout = QHBoxLayout(pass_wrap)
        pass_layout.setObjectName("Password{}".format(idx + 1))

        label1 = QLabel(pass_wrap)
        label1.setText(password)

        label2 = QLabel(pass_wrap)
        label2.setText(password)

        label3 = QLabel(pass_wrap)
        label3.setText(password)

        checkbox = QCheckBox(pass_wrap)
        checkbox.setChecked(False)
        checkbox.setObjectName("CheckBox{}".format(idx + 1))
        # checkbox.checkStateChanged.connect(self.checkbox_state_changed)

        pass_layout.addWidget(label1)
        pass_layout.addWidget(label2)
        pass_layout.addWidget(label3)
        pass_layout.addWidget(checkbox)

        if idx % 2 == 0:
            pass_wrap.setStyleSheet("background-color: #f0f0f0")
        else:
            pass_wrap.setStyleSheet("background-color: #4CAF50")

        Array_passwords = np.append(Array_passwords, pass_wrap)
        print(password)
        if idx == 9:
            break

    for label_ in Array_passwords:
        self.layout.addWidget(label_)