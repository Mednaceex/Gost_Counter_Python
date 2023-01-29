from PyQt5 import QtCore, QtWidgets

from modules.custom_config import get_player_count
width, height = (756, 791)


class TeamsDialog(object):
    def __init__(self, dialog):
        dialog.resize(width, height)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(int(280 * width/756), int(750 * height/791),
                                                int(201 * width/756), int(32 * height/791)))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.Main = QtWidgets.QScrollArea(dialog)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(dialog)
        self.title_widget = QtWidgets.QWidget(dialog)
        self.set_size()
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(False)
        self.Main.setWidget(self.scrollAreaWidgetContents)

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
        self.set_teams()

        self._translate = QtCore.QCoreApplication.translate
        self.retranslate_ui()
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        for i in range(get_player_count()):
            self.label[i].setText(self._translate("Dialog", f"{i + 1}."))
        self.label_team_name.setText(self._translate("Dialog", "Название команды"))
        self.label_coach_name.setText(self._translate("Dialog", "Тренер"))

    def set_spacers(self):
        self.spacers = []
        for i in range(get_player_count()):
            self.spacers.append(QtWidgets.QSpacerItem(int(25 * width / 756), int(20 * height / 791)))
            self.spacers.append(QtWidgets.QSpacerItem(int(6 * width/756), int(20 * height/791)))

    def set_teams(self):
        self.label = []
        self.teams = []
        self.names = []
        self.set_spacers()
        for i in range(get_player_count()):
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
        for item in self.teams:
            self.teams_layout.removeWidget(item)
        for item in self.names:
            self.teams_layout.removeWidget(item)
        for item in self.label:
            item.clear()
        for child in self.teams_layout.children():
            child.deleteLater()

    def update_settings(self):
        self.remove_teams()
        self.set_size()
        self.set_teams()
        self.retranslate_ui()

    def set_size(self):
        self.Main.setGeometry(QtCore.QRect(int(10 * width/756), int(37 * height/791),
                                           int(738 * width/756), int(698 * height/791)))
        self.scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(int(10 * width/756), 0, int(715 * width/756), int(742 * height * get_player_count()/15820)))
        self.title_widget.setGeometry(QtCore.QRect(int(10 * width/756), int(2 * height/791),
                                                   int(738 * width/756), int(30 * height/791)))
