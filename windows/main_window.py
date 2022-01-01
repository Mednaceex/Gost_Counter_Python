from PyQt5 import QtCore, QtWidgets


class MainWindow(object):
    def __init__(self, main_window):
        main_window.setEnabled(True)
        main_window.resize(1204, 881)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.Main = QtWidgets.QScrollArea(self.central_widget)
        self.Main.setGeometry(QtCore.QRect(10, 140, 1191, 631))
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(True)
        self.scrollAreaWidgetContents_82 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_82.setGeometry(QtCore.QRect(0, 0, 1170, 3175))
        self.verticalLayout_119 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_82)
        size_policy_exp_fixed = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy_exp_fixed.setHorizontalStretch(0)
        size_policy_exp_fixed.setVerticalStretch(0)
        self.box_list = []
        for i in range(10):
            row = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_82)
            size_policy_exp_fixed.setHeightForWidth(row.sizePolicy().hasHeightForWidth())
            row.setSizePolicy(size_policy_exp_fixed)
            row.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1148, 309))
            horizontal_layout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
            for k in range(2):
                box = Box()
                horizontal_layout.addWidget(box)
                self.box_list.append(box)
            row.setWidget(self.scrollAreaWidgetContents)
            self.verticalLayout_119.addWidget(row)
        self.Main.setWidget(self.scrollAreaWidgetContents_82)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(270, 786, 647, 50))
        self.Button_Layout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.Save_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_Layout.addWidget(self.Save_Button)
        self.Count_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_Layout.addWidget(self.Count_Button)
        self.Reset_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_Layout.addWidget(self.Reset_Button)
        self.verticalLayoutWidget_22 = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget_22.setGeometry(QtCore.QRect(108, 10, 971, 50))
        self.Button_Layout_2 = QtWidgets.QHBoxLayout(self.verticalLayoutWidget_22)
        self.Matches_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_22)
        self.Button_Layout_2.addWidget(self.Matches_Button)
        self.Teams_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_22)
        self.Button_Layout_2.addWidget(self.Teams_Button)
        self.Settings_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_22)
        self.Button_Layout_2.addWidget(self.Settings_Button)
        self.widget = QtWidgets.QWidget(self.central_widget)
        self.widget.setGeometry(QtCore.QRect(30, 70, 1131, 53))
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.match_labels = []
        self.two_dots_labels = []
        self.scores = []
        for i in range(10):
            vertical_layout = QtWidgets.QVBoxLayout()
            vertical_layout.setContentsMargins(-1, 0, -1, -1)
            self.match_labels.append(QtWidgets.QLabel(self.widget))
            vertical_layout.addWidget(self.match_labels[i], 0, QtCore.Qt.AlignHCenter)
            score_layout = QtWidgets.QHBoxLayout()
            score_layout.setContentsMargins(-1, -1, -1, 0)
            self.scores.append([QtWidgets.QLineEdit(self.widget), QtWidgets.QLineEdit(self.widget)])
            for j in range(2):
                self.scores[i][j].setAlignment(QtCore.Qt.AlignCenter)
            score_layout.addWidget(self.scores[i][0])
            self.two_dots_labels.append(QtWidgets.QLabel(self.widget))
            score_layout.addWidget(self.two_dots_labels[i])
            score_layout.addWidget(self.scores[i][1])
            vertical_layout.addLayout(score_layout)
            self.horizontalLayout_33.addLayout(vertical_layout)
            if i < 9:
                spacer = QtWidgets.QSpacerItem(15, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.horizontalLayout_33.addItem(spacer)

        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1204, 26))
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        for i in range(20):
            self.box_list[i].name.setText(_translate("MainWindow", f"{i + 1}"))
            for j in range(10):
                self.box_list[i].labels[j].setText(_translate("MainWindow", f"{j + 1}"))
        self.Save_Button.setText(_translate("MainWindow", "Сохранить"))
        self.Count_Button.setText(_translate("MainWindow", "Рассчитать"))
        self.Reset_Button.setText(_translate("MainWindow", "Очистить"))
        self.Matches_Button.setText(_translate("MainWindow", "Настроить матчи"))
        self.Teams_Button.setText(_translate("MainWindow", "Изменить команды"))
        self.Settings_Button.setText(_translate("MainWindow", "Настройки"))
        for i in range(10):
            self.match_labels[i].setText(_translate("MainWindow", f"Матч {i + 1}"))
            self.two_dots_labels[i].setText(_translate("MainWindow", ":"))


class Box(QtWidgets.QWidget):
    def __init__(self):
        super(Box, self).__init__()
        self.setGeometry(QtCore.QRect(0, 0, 560, 287))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.name = QtWidgets.QLabel(self)
        self.verticalLayout.addWidget(self.name)
        self.text = QtWidgets.QTextEdit(self)
        self.text.setStyleSheet("border: 1px solid gray")
        self.verticalLayout.addWidget(self.text)
        checks_layout = QtWidgets.QHBoxLayout()
        checks_layout.setContentsMargins(-1, -1, -1, 0)
        self.labels = []
        self.checks = []
        for j in range(10):
            check_layout = QtWidgets.QVBoxLayout()
            check_layout.setContentsMargins(-1, -1, 0, 0)
            self.labels.append(QtWidgets.QLabel(self))
            check_layout.addWidget(self.labels[j], 0, QtCore.Qt.AlignHCenter)
            self.checks.append(QtWidgets.QCheckBox(self))
            self.checks[j].setText("")
            check_layout.addWidget(self.checks[j], 0, QtCore.Qt.AlignHCenter)
            checks_layout.addLayout(check_layout)
        self.verticalLayout.addLayout(checks_layout)
