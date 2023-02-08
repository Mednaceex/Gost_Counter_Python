from PyQt5 import QtCore, QtWidgets

from modules.classes import ConfirmDialogUI

width, height = (756, 791)


class TeamsUI(ConfirmDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса диалогового окна настройки команд
        :param dialog: окно настройки команд
        """
        super().__init__(dialog)
        self.dialog = dialog
        self.league = dialog.league
        dialog.resize(width, height)

        # Задание основного виджета и области с прокруткой
        self.Main = QtWidgets.QScrollArea(dialog)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(dialog)
        self.title_widget = QtWidgets.QWidget(dialog)
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(False)
        self.Main.setWidget(self.scrollAreaWidgetContents)

        # Инициализация атрибутов класса
        self.spacers = []
        self.label = []
        self.teams = []
        self.names = []

        # Создание заголовочного виджета с подписями "Название команды" и "Тренер"
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.spacing_layout = QtWidgets.QVBoxLayout()
        self.spacing_layout.setContentsMargins(-1, -1, -1, 0)
        self.spacing_layout.setSpacing(int(8 * height/791))
        size_policy_preferred = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy_preferred.setHorizontalStretch(0)
        size_policy_preferred.setVerticalStretch(0)
        self.title_layout = QtWidgets.QHBoxLayout(self.title_widget)
        self.title_layout.setContentsMargins(-1, -1, -1, 0)
        self.title_layout.setSpacing(0)
        self.label_team_name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.title_layout.addWidget(self.label_team_name, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label_coach_name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.title_layout.addWidget(self.label_coach_name, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.teams_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.set_teams()  # Создание строк для ввода команд
        self.set_size()
        self.set_standard_buttons()

        self._translate = QtCore.QCoreApplication.translate
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        for i in range(self.league.get_player_count()):
            self.label[i].setText(self._translate("Dialog", f"{i + 1}."))
        self.label_team_name.setText(self._translate("Dialog", "Название команды"))
        self.label_coach_name.setText(self._translate("Dialog", "Тренер"))

    def set_spacers(self):
        """
        Создаёт виджеты для отступа перед каждой из строк для ввода текста
        """
        self.spacers = []
        for i in range(self.league.get_player_count()):
            self.spacers.append(QtWidgets.QSpacerItem(int(25 * width / 756), int(20 * height / 791)))
            self.spacers.append(QtWidgets.QSpacerItem(int(6 * width/756), int(20 * height/791)))

    def set_teams(self):
        """
        Создаёт пустые поля с названиями команд и именами тренеров
        """
        self.label = []
        self.teams = []
        self.names = []
        self.set_spacers()
        for i in range(self.league.get_player_count()):
            horizontal_layout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
            self.label.append(QtWidgets.QLabel(self.scrollAreaWidgetContents))
            self.label[i].setFixedWidth(20)
            horizontal_layout.addWidget(self.label[i])
            for line_list in (self.teams, self.names):
                line_list.append(QtWidgets.QLineEdit(self.scrollAreaWidgetContents))
            horizontal_layout.addWidget(self.teams[i])
            horizontal_layout.addItem(self.spacers[2*i])
            horizontal_layout.addWidget(self.names[i])
            self.spacers.append(QtWidgets.QSpacerItem(int(6 * width/756), int(20 * height/791)))
            horizontal_layout.addItem(self.spacers[2*i+1])
            self.teams_layout.addLayout(horizontal_layout)

    def remove_teams(self):
        """
        Удаляет все поля с названиями команд и именами тренеров
        """
        for item in self.teams:
            self.teams_layout.removeWidget(item)
        for item in self.names:
            self.teams_layout.removeWidget(item)
        for item in self.label:
            item.clear()
        for child in self.teams_layout.children():
            child.deleteLater()

    def update_settings(self):
        """
        Обновляет настройки окна в соответствии с текущей лигой, выбранной в главном окне
        """
        self.remove_teams()
        self.league = self.dialog.league
        self.set_size()
        self.set_teams()
        self.retranslate_ui()

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.button_widget.setGeometry(QtCore.QRect(int(240 * width/756), int(728 * height/791),
                                                    int(281 * width/756), int(50 * height/791)))
        self.Main.setGeometry(QtCore.QRect(int(10 * width/756), int(37 * height/791),
                                           int(738 * width/756), int(698 * height/791)))
        self.scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(int(10 * width/756), 0, int(715 * width/756),
                         int(742 * height * self.league.get_player_count()/15820)))
        self.title_widget.setGeometry(QtCore.QRect(int(10 * width/756), int(2 * height/791),
                                                   int(738 * width/756), int(30 * height/791)))
