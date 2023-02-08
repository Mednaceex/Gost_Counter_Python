from PyQt5 import QtCore, QtWidgets
from modules.custom_config import get_current_league
from modules.templates import Box

width, height = (1204, 881)


class MainWindowUI:
    def __init__(self, main_window):
        """
        Конструктор графического интерфейса главного окна

        :param main_window: главное окно
        """
        self.main_window = main_window
        self.update_league()
        main_window.setEnabled(True)
        main_window.resize(width, height)
        self.central_widget = QtWidgets.QWidget(main_window)
        main_window.setCentralWidget(self.central_widget)
        self.Main = QtWidgets.QScrollArea(self.central_widget)
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(True)
        self.scroll_area_contents = QtWidgets.QWidget()
        self.size_policy_exp_fixed = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.size_policy_exp_fixed.setHorizontalStretch(0)
        self.size_policy_exp_fixed.setVerticalStretch(0)
        self.Main.setWidget(self.scroll_area_contents)

        # Инициализация атрибутов класса
        self.bottom_buttons_widget = QtWidgets.QWidget(self.central_widget)
        self.top_buttons_widget = QtWidgets.QWidget(self.central_widget)
        self.matches_widget = QtWidgets.QWidget(self.central_widget)
        self.matchLayout = QtWidgets.QHBoxLayout(self.matches_widget)
        self.additional_layout = QtWidgets.QVBoxLayout(self.matches_widget)
        self.add_label = QtWidgets.QLabel(self.matches_widget)
        self.add_yes_label = QtWidgets.QLabel(self.matches_widget)
        self.add_no_label = QtWidgets.QLabel(self.matches_widget)
        self.add_yes_box = QtWidgets.QCheckBox(self.matches_widget)
        self.add_no_box = QtWidgets.QCheckBox(self.matches_widget)
        self.boxLayout = QtWidgets.QVBoxLayout(self.scroll_area_contents)
        self.add_bets = []
        self.match_labels = []
        self.two_dots_labels = []
        self.scores = []
        self.spacers = []
        self.box_list = []
        self.league = self.main_window.league

        # Настройка отображения нужных элементов
        self.add_yes_box.hide()
        self.add_no_box.hide()
        self.init_boxes()
        self.init_matches()
        self.set_additional()
        if self.league.get_has_additional():
            self.init_additional()

        # Основные параметры области прокрутки и стандартные параметры главного окна
        self.menubar = QtWidgets.QMenuBar(main_window)
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        # Инициализация кнопок
        self.bottom_button_layout = QtWidgets.QHBoxLayout(self.bottom_buttons_widget)
        self.Save_Button = QtWidgets.QPushButton(self.bottom_buttons_widget)
        self.bottom_button_layout.addWidget(self.Save_Button)
        self.Count_Button = QtWidgets.QPushButton(self.bottom_buttons_widget)
        self.bottom_button_layout.addWidget(self.Count_Button)
        self.Reset_Button = QtWidgets.QPushButton(self.bottom_buttons_widget)
        self.bottom_button_layout.addWidget(self.Reset_Button)
        self.top_button_layout = QtWidgets.QHBoxLayout(self.top_buttons_widget)
        self.Matches_Button = QtWidgets.QPushButton(self.top_buttons_widget)
        self.top_button_layout.addWidget(self.Matches_Button)
        self.Teams_Button = QtWidgets.QPushButton(self.top_buttons_widget)
        self.top_button_layout.addWidget(self.Teams_Button)
        self.Settings_Button = QtWidgets.QPushButton(self.top_buttons_widget)
        self.top_button_layout.addWidget(self.Settings_Button)
        self.Leagues_Button = QtWidgets.QPushButton(self.top_buttons_widget)
        self.top_button_layout.addWidget(self.Leagues_Button)

        self.set_size()
        self._translate = QtCore.QCoreApplication.translate
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self):
        self.retranslate_boxes()
        self.retranslate_buttons()
        self.retranslate_matches()
        if self.league.get_has_additional():
            self.retranslate_additional()

    def retranslate_boxes(self):
        for i in range(self.league.get_player_count()):
            self.box_list[i].name.setText(self._translate("MainWindow", f"{i + 1}"))
            for j in range(self.league.get_match_count()):
                self.box_list[i].labels[j].setText(self._translate("MainWindow", f"{j + 1}"))
            if self.league.get_has_additional():
                self.box_list[i].add_yes_label.setText(self._translate("MainWindow", "Да"))
                self.box_list[i].add_no_label.setText(self._translate("MainWindow", "Нет"))
                self.box_list[i].add_label.setText(self._translate("MainWindow", "Доп. ставка"))

    def retranslate_matches(self):
        for i in range(self.league.get_match_count()):
            self.match_labels[i].setText(self._translate("MainWindow", f"Матч {i + 1}"))
            self.two_dots_labels[i].setText(self._translate("MainWindow", ":"))

    def retranslate_additional(self):
        self.add_label.setText(self._translate("MainWindow", "Дополнительная ставка"))
        self.add_yes_label.setText(self._translate("MainWindow", "Да"))
        self.add_no_label.setText(self._translate("MainWindow", "Нет"))

    def retranslate_buttons(self):
        self.Save_Button.setText(self._translate("MainWindow", "Сохранить"))
        self.Count_Button.setText(self._translate("MainWindow", "Рассчитать"))
        self.Reset_Button.setText(self._translate("MainWindow", "Очистить"))
        self.Matches_Button.setText(self._translate("MainWindow", "Настроить матчи"))
        self.Teams_Button.setText(self._translate("MainWindow", "Изменить команды"))
        self.Settings_Button.setText(self._translate("MainWindow", "Настройки"))
        self.Leagues_Button.setText(self._translate("MainWindow", f"Текущая лига: {self.league.name}"))

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.Main.setGeometry(QtCore.QRect(int(10 * width/1204), int(140 * height/881),
                                           int(1191 * width/1204), int(631 * height/881)))
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, int(1170 * width/1204), int(3175 * height/881)))
        self.bottom_buttons_widget.setGeometry(QtCore.QRect(int(270 * width/1204), int(786 * height/881),
                                                            int(647 * width/1204), int(50 * height/881)))
        self.top_buttons_widget.setGeometry(QtCore.QRect(int(108 * width/1204), int(10 * height/881),
                                                              int(971 * width/1204), int(50 * height/881)))
        self.matches_widget.setGeometry(QtCore.QRect(int(30 * width/1204), int(62 * height/881),
                                                     int(1131 * width/1204), int(75 * height/881)))
        self.menubar.setGeometry(QtCore.QRect(0, 0, int(1204 * width/1204), int(26 * height/881)))

    def set_league_name(self, league_name: str):
        """
        Меняет название лиги на кнопке

        :param league_name: новое название лиги
        """
        self.Leagues_Button.setText(self._translate("MainWindow", f"Текущая лига: {league_name}"))

    def update_league(self):
        """
        Обновляет лигу в соответствии с лигой главного окна
        """
        self.league = self.main_window.league

    def update_settings(self):
        """
        Обновляет настройки в соответствии с текущей лигой
        """
        self.remove_matches()
        self.remove_additional()
        self.remove_boxes()
        self.init_matches()
        self.init_boxes()
        self.retranslate_boxes()
        self.retranslate_matches()
        if self.league.get_has_additional():
            self.init_additional()
            self.retranslate_additional()
        self.set_league_name(self.league.name)

    def remove_additional(self):
        """
        Удаляет окно дополнительной ставки с галочками в строке результатов матчей
        """
        self.matchLayout.removeItem(self.additional_layout)
        self.add_label.setText(self._translate("MainWindow", ""))
        self.add_yes_label.setText(self._translate("MainWindow", ""))
        self.add_no_label.setText(self._translate("MainWindow", ""))
        self.add_yes_box.hide()
        self.add_no_box.hide()

    def remove_boxes(self):
        """
        Удаляет окна ввода текстов гостов
        """
        while self.boxLayout.count():
            self.boxLayout.takeAt(0).widget().setParent(None)

    def remove_matches(self):
        """
        Удаляет окна ввода счетов матчей
        """
        for i, label in enumerate(self.match_labels):
            self.matchLayout.removeWidget(label)
            self.matchLayout.removeWidget(self.two_dots_labels[i])
            for j in range(2):
                self.matchLayout.removeWidget(self.scores[i][j])
        for spacer in self.spacers:
            self.matchLayout.removeItem(spacer)

    def init_boxes(self):
        """
        Создаёт окна ввода текстов гостов
        """
        self.box_list = []
        for i in range(int(self.league.get_player_count() / 2)):
            row = QtWidgets.QScrollArea(self.scroll_area_contents)
            self.size_policy_exp_fixed.setHeightForWidth(row.sizePolicy().hasHeightForWidth())
            row.setSizePolicy(self.size_policy_exp_fixed)
            row.setWidgetResizable(True)
            scroll_area_contents = QtWidgets.QWidget()
            scroll_area_contents.setGeometry(QtCore.QRect(0, 0, int(114 * width/1204), int(30 * height/881)))
            horizontal_layout = QtWidgets.QHBoxLayout(scroll_area_contents)
            for k in range(2):
                box = Box(width, height, self.league.get_match_count(), self.league.get_has_additional())
                horizontal_layout.addWidget(box)
                self.box_list.append(box)
            row.setWidget(scroll_area_contents)
            self.boxLayout.addWidget(row)
        if self.league.get_player_count() % 2 == 1:
            box = Box(width, height, self.league.get_match_count(), self.league.get_has_additional())
            self.box_list.append(box)
            self.boxLayout.addWidget(box)

    def init_matches(self):
        """
        Создаёт окна ввода счетов матчей
        """
        self.match_labels = []
        self.two_dots_labels = []
        self.scores = []
        self.spacers = []
        for i in range(self.league.get_match_count()):
            vertical_layout = QtWidgets.QVBoxLayout()
            vertical_layout.setContentsMargins(-1, 0, -1, -1)
            self.match_labels.append(QtWidgets.QLabel(self.matches_widget))
            vertical_layout.addWidget(self.match_labels[i], 0, QtCore.Qt.AlignHCenter)
            score_layout = QtWidgets.QHBoxLayout()
            score_layout.setContentsMargins(-1, -1, -1, 0)
            self.scores.append([QtWidgets.QLineEdit(self.matches_widget), QtWidgets.QLineEdit(self.matches_widget)])
            for j in range(2):
                self.scores[i][j].setAlignment(QtCore.Qt.AlignCenter)
            score_layout.addWidget(self.scores[i][0])
            self.two_dots_labels.append(QtWidgets.QLabel(self.matches_widget))
            score_layout.addWidget(self.two_dots_labels[i])
            score_layout.addWidget(self.scores[i][1])
            vertical_layout.addLayout(score_layout)
            self.matchLayout.addLayout(vertical_layout)
            if i < self.league.get_match_count() - 1:
                spacer = QtWidgets.QSpacerItem(int(15 * width/1204), int(40 * height/881),
                                               QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                self.matchLayout.addItem(spacer)
                self.spacers.append(spacer)

    def init_additional(self):
        """
        Создаёт окно дополнительной ставки с галочками в строке результатов матчей
        """
        self.add_yes_box.show()
        self.add_no_box.show()
        self.matchLayout.addLayout(self.additional_layout)

    def set_additional(self):
        """
        Создаёт окошки с галочками для дополнительной ставки
        """
        additional_yes_layout = QtWidgets.QVBoxLayout()
        additional_no_layout = QtWidgets.QVBoxLayout()
        additional_bet_horizontal_layout = QtWidgets.QHBoxLayout()
        additional_yes_layout.addWidget(self.add_yes_label, 0, QtCore.Qt.AlignHCenter)
        additional_yes_layout.addWidget(self.add_yes_box, 0, QtCore.Qt.AlignHCenter)
        additional_no_layout.addWidget(self.add_no_label, 0, QtCore.Qt.AlignHCenter)
        additional_no_layout.addWidget(self.add_no_box, 0, QtCore.Qt.AlignHCenter)
        additional_bet_horizontal_layout.addLayout(additional_yes_layout)
        additional_bet_horizontal_layout.addLayout(additional_no_layout)
        self.additional_layout.addWidget(self.add_label, 0, QtCore.Qt.AlignHCenter)
        self.additional_layout.addLayout(additional_bet_horizontal_layout)
