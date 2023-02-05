from PyQt5 import QtCore, QtWidgets

from modules.templates import Line
width, height = (924, 667)


class MatchesDialog:
    def __init__(self, dialog):
        self.dialog = dialog
        dialog.resize(width, height)
        self.league = dialog.league
        self.central_widget = QtWidgets.QWidget()

        self.Main = QtWidgets.QScrollArea(self.central_widget)
        self.Main.setStyleSheet("border: 0")
        self.Main.setWidgetResizable(False)
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.Main)
        self.Main.setWidget(self.scrollAreaWidgetContents)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.central_widget)
        self.buttonBox.setGeometry(QtCore.QRect(int(350 * width/924), int(560 * height/667),
                                                int(201 * width/924), int(32 * height/667)))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.teams = []
        for i in range(int(self.league.get_player_count() / 2)):
            self.teams.append([])
            horizontal_layout = QtWidgets.QHBoxLayout()
            for j in range(2):
                box = QtWidgets.QComboBox(self.verticalLayoutWidget)
                self.teams[i].append(box)
                horizontal_layout.addWidget(self.teams[i][j])
            self.verticalLayout.addLayout(horizontal_layout)

        self.field_factor = Line(self.scrollAreaWidgetContents, QtWidgets.QCheckBox(self.scrollAreaWidgetContents))
        self.set_size()

        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        self.layout = QtWidgets.QGridLayout(dialog)
        self.layout.addWidget(self.central_widget, 0, 0)

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.field_factor.label.setText(_translate("Dialog", "Домашний фактор"))

    def update_settings(self):
        self.league = self.dialog.league
        for pair in self.teams:
            for item in pair:
                self.verticalLayout.removeWidget(item)
        self.set_size()
        self.teams = []
        for i in range(int(self.league.get_player_count() / 2)):
            self.teams.append([])
            horizontal_layout = QtWidgets.QHBoxLayout()
            for j in range(2):
                self.teams[i].append(QtWidgets.QComboBox(self.verticalLayoutWidget))
                horizontal_layout.addWidget(self.teams[i][j])
            self.verticalLayout.addLayout(horizontal_layout)

    def set_size(self):
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(
            int(5 * width/924), int(0 * height/667), int(826 * width/924),
            int(481 * height * (self.league.get_player_count()/2) / 6670)))
        self.field_factor.align(32 * width / 924, 160 * width / 924,
                                int(((481 * (self.league.get_player_count()/2)) - 50) * height / 6670),
                                555 * width / 924, 20 * height / 667)
        self.Main.setGeometry(QtCore.QRect(int(20 * width/924), int(10 * height/667),
                                           int(875 * width/924), int(526 * height/667)))
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(
            0, 0, int(840 * width/924), int((481 * (self.league.get_player_count()/2) + 350) * height / 6670)))
