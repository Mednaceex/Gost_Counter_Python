from PyQt5 import QtCore, QtWidgets

from modules.templates import Line
from modules.classes import ConfirmDialogUI

width, height = (924, 667)


class MatchesUI(ConfirmDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна настройки матчей

        :param dialog: окно настройки матчей
        """
        super().__init__(dialog)
        self.dialog = dialog
        dialog.resize(width, height)
        self.league = dialog.league
        self.central_widget = QtWidgets.QWidget(dialog)

        self.Main = QtWidgets.QScrollArea(self.central_widget)
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(False)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.Main)
        self.Main.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.teams = []
        self.init_combo_boxes()
        self.field_factor = Line(self.scrollAreaWidgetContents, QtWidgets.QCheckBox(self.scrollAreaWidgetContents))

        self.set_size()
        self.set_standard_buttons()
        self.field_factor.label.setText(QtCore.QCoreApplication.translate("Dialog", "Домашний фактор"))
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def update_settings(self):
        """
        Обновляет настройки окна в соответствии с текущей лигой, выбранной в главном окне
        """
        self.league = self.dialog.league
        self.remove_combo_boxes()
        self.set_size()
        self.init_combo_boxes()

    def remove_combo_boxes(self):
        """
        Удаляет выпадающие списки команд
        """
        for pair in self.teams:
            for item in pair:
                self.verticalLayout.removeWidget(item)

    def init_combo_boxes(self):
        """
        Создаёт выпадающие списки команд
        """
        self.teams = []
        for i in range(int(self.league.get_player_count() / 2)):
            self.teams.append([])
            horizontal_layout = QtWidgets.QHBoxLayout()
            for j in range(2):
                box = QtWidgets.QComboBox(self.verticalLayoutWidget)
                self.teams[i].append(box)
                horizontal_layout.addWidget(self.teams[i][j])
            self.verticalLayout.addLayout(horizontal_layout)

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.button_widget.setGeometry(QtCore.QRect(int(310 * width/924), int(540 * height/667),
                                                    int(281 * width/924), int(52 * height/667)))
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(
            int(5 * width/924), int(0 * height/667), int(826 * width/924),
            int(481 * height * (self.league.get_player_count()/2) / 6670)))
        self.field_factor.align(int(32 * width / 924), int(160 * width / 924),
                                int(((481 * (self.league.get_player_count()/2)) - 50) * height / 6670),
                                int(555 * width / 924), int(20 * height / 667))
        self.Main.setGeometry(QtCore.QRect(int(20 * width/924), int(10 * height/667),
                                           int(875 * width/924), int(526 * height/667)))
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(
            0, 0, int(840 * width/924), int((481 * (self.league.get_player_count()/2) + 350) * height / 6670)))
