from PyQt5 import QtCore, QtWidgets

from modules.custom_config import get_player_count, get_match_count, get_has_additional
width, height = (1204, 881)


class MainWindow(object):
    def __init__(self, main_window):
        main_window.setEnabled(True)
        main_window.resize(width, height)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.Main = QtWidgets.QScrollArea(self.central_widget)
        self.Main.setGeometry(QtCore.QRect(int(10 * width/1204), int(140 * height/881),
                                           int(1191 * width/1204), int(631 * height/881)))
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(True)
        self.scrollAreaWidgetContents_82 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_82.setGeometry(QtCore.QRect(0, 0, int(1170 * width/1204), int(3175 * height/881)))
        self.verticalLayout_119 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_82)
        size_policy_exp_fixed = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy_exp_fixed.setHorizontalStretch(0)
        size_policy_exp_fixed.setVerticalStretch(0)
        self.box_list = []
        for i in range(int(get_player_count() / 2)):
            row = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_82)
            size_policy_exp_fixed.setHeightForWidth(row.sizePolicy().hasHeightForWidth())
            row.setSizePolicy(size_policy_exp_fixed)
            row.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, int(1148 * width/1204), int(309 * height/881)))
            horizontal_layout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
            for k in range(2):
                box = Box()
                horizontal_layout.addWidget(box)
                self.box_list.append(box)
            row.setWidget(self.scrollAreaWidgetContents)
            self.verticalLayout_119.addWidget(row)
        if get_player_count() % 2 == 1:
            box = Box()
            self.box_list.append(box)
            self.verticalLayout_119.addWidget(box)
        self.Main.setWidget(self.scrollAreaWidgetContents_82)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(int(270 * width/1204), int(786 * height/881),
                                                           int(647 * width/1204), int(50 * height/881)))
        self.Button_Layout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.Save_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_Layout.addWidget(self.Save_Button)
        self.Count_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_Layout.addWidget(self.Count_Button)
        self.Reset_Button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_Layout.addWidget(self.Reset_Button)
        self.verticalLayoutWidget_22 = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget_22.setGeometry(QtCore.QRect(int(108 * width/1204), int(10 * height/881),
                                                              int(971 * width/1204), int(50 * height/881)))
        self.Button_Layout_2 = QtWidgets.QHBoxLayout(self.verticalLayoutWidget_22)
        self.Matches_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_22)
        self.Button_Layout_2.addWidget(self.Matches_Button)
        self.Teams_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_22)
        self.Button_Layout_2.addWidget(self.Teams_Button)
        self.Settings_Button = QtWidgets.QPushButton(self.verticalLayoutWidget_22)
        self.Button_Layout_2.addWidget(self.Settings_Button)
        self.widget = QtWidgets.QWidget(self.central_widget)
        self.widget.setGeometry(QtCore.QRect(int(30 * width/1204), int(62 * height/881),
                                             int(1131 * width/1204), int(75 * height/881)))
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.widget)
        self.match_labels = []
        self.two_dots_labels = []
        self.scores = []
        self.add_bets = []
        for i in range(get_match_count()):
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
                spacer = QtWidgets.QSpacerItem(int(15 * width/1204), int(40 * height/881),
                                               QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.horizontalLayout_33.addItem(spacer)

        if get_has_additional():
            additional_bet_layout = QtWidgets.QVBoxLayout()
            additional_yes_layout = QtWidgets.QVBoxLayout()
            additional_no_layout = QtWidgets.QVBoxLayout()
            additional_bet_horizontal_layout = QtWidgets.QHBoxLayout()
            self.add_label = QtWidgets.QLabel(self.widget)
            self.add_yes_label = QtWidgets.QLabel(self.widget)
            self.add_no_label = QtWidgets.QLabel(self.widget)
            self.add_yes_box = QtWidgets.QCheckBox(self.widget)
            self.add_no_box = QtWidgets.QCheckBox(self.widget)
            additional_yes_layout.addWidget(self.add_yes_label, 0, QtCore.Qt.AlignHCenter)
            additional_yes_layout.addWidget(self.add_yes_box, 0, QtCore.Qt.AlignHCenter)
            additional_no_layout.addWidget(self.add_no_label, 0, QtCore.Qt.AlignHCenter)
            additional_no_layout.addWidget(self.add_no_box, 0, QtCore.Qt.AlignHCenter)
            additional_bet_horizontal_layout.addLayout(additional_yes_layout)
            additional_bet_horizontal_layout.addLayout(additional_no_layout)
            additional_bet_layout.addWidget(self.add_label, 0, QtCore.Qt.AlignHCenter)
            additional_bet_layout.addLayout(additional_bet_horizontal_layout)
            self.horizontalLayout_33.addLayout(additional_bet_layout)

        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, int(1204 * width/1204), int(26 * height/881)))
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(get_player_count()):
            self.box_list[i].name.setText(_translate("MainWindow", f"{i + 1}"))
            for j in range(get_match_count()):
                self.box_list[i].labels[j].setText(_translate("MainWindow", f"{j + 1}"))
            if get_has_additional():
                self.box_list[i].add_yes_label.setText(_translate("MainWindow", "Да"))
                self.box_list[i].add_no_label.setText(_translate("MainWindow", "Нет"))
                self.box_list[i].add_label.setText(_translate("MainWindow", "Доп. ставка"))
        self.Save_Button.setText(_translate("MainWindow", "Сохранить"))
        self.Count_Button.setText(_translate("MainWindow", "Рассчитать"))
        self.Reset_Button.setText(_translate("MainWindow", "Очистить"))
        self.Matches_Button.setText(_translate("MainWindow", "Настроить матчи"))
        self.Teams_Button.setText(_translate("MainWindow", "Изменить команды"))
        self.Settings_Button.setText(_translate("MainWindow", "Настройки"))
        if get_has_additional():
            self.add_label.setText(_translate("MainWindow", "Дополнительная ставка"))
            self.add_yes_label.setText(_translate("MainWindow", "Да"))
            self.add_no_label.setText(_translate("MainWindow", "Нет"))
        for i in range(get_match_count()):
            self.match_labels[i].setText(_translate("MainWindow", f"Матч {i + 1}"))
            self.two_dots_labels[i].setText(_translate("MainWindow", ":"))

    def update_settings(self, main_window):
        pass


class Box(QtWidgets.QWidget):
    def __init__(self):
        super(Box, self).__init__()
        self.setGeometry(QtCore.QRect(0, 0, int(560 * width/1204), int(287 * height/881)))
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
        for j in range(get_match_count()):
            check_layout = QtWidgets.QVBoxLayout()
            check_layout.setContentsMargins(-1, -1, 0, 0)
            self.labels.append(QtWidgets.QLabel(self))
            check_layout.addWidget(self.labels[j], 0, QtCore.Qt.AlignHCenter)
            self.checks.append(QtWidgets.QCheckBox(self))
            self.checks[j].setText("")
            check_layout.addWidget(self.checks[j], 0, QtCore.Qt.AlignHCenter)
            checks_layout.addLayout(check_layout)
        self.verticalLayout.addLayout(checks_layout)

        if get_has_additional():
            self.add_yes = QtWidgets.QCheckBox(self)
            self.add_no = QtWidgets.QCheckBox(self)
            self.add_yes_label = QtWidgets.QLabel(self)
            self.add_no_label = QtWidgets.QLabel(self)
            self.add_label = QtWidgets.QLabel(self)

            additional_bet_layout = QtWidgets.QVBoxLayout()
            additional_yes_layout = QtWidgets.QHBoxLayout()
            additional_no_layout = QtWidgets.QHBoxLayout()
            additional_yes_layout.addWidget(self.add_yes_label, 0, QtCore.Qt.AlignHCenter)
            additional_yes_layout.addWidget(self.add_yes, 0, QtCore.Qt.AlignHCenter)
            additional_no_layout.addWidget(self.add_no_label, 0, QtCore.Qt.AlignHCenter)
            additional_no_layout.addWidget(self.add_no, 0, QtCore.Qt.AlignHCenter)
            additional_bet_layout.addWidget(self.add_label, 0, QtCore.Qt.AlignHCenter)
            additional_bet_layout.addLayout(additional_yes_layout)
            additional_bet_layout.addLayout(additional_no_layout)
            checks_layout.addLayout(additional_bet_layout)

            self.add_yes.clicked.connect(self.clear_additional_no)
            self.add_no.clicked.connect(self.clear_additional_yes)

    def clear_additional_yes(self):
        """
        Снимает галочку "Да" в окошке дополнительной ставки
        """
        self.add_yes.setCheckState(QtCore.Qt.Unchecked)

    def clear_additional_no(self):
        """
        Снимает галочку "Нет" в окошке дополнительной ставки
        """
        self.add_no.setCheckState(QtCore.Qt.Unchecked)
