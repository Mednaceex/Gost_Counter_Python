from PyQt5 import QtCore, QtWidgets

from modules.custom_config import player_count
width, height = (924, 667)


class MatchesDialog(object):
    def __init__(self, dialog):
        dialog.resize(width, height)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(int(350 * width/924), int(560 * height/667),
                                                int(201 * width/924), int(32 * height/667)))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayoutWidget = QtWidgets.QWidget(dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(int(20 * width/924), int(30 * height/667),
                                                           int(881 * width/924), int(481 * height/667)))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.teams = []
        for i in range(int(player_count / 2)):
            self.teams.append([])
            horizontal_layout = QtWidgets.QHBoxLayout()
            for j in range(2):
                self.teams[i].append(QtWidgets.QComboBox(self.verticalLayoutWidget))
                horizontal_layout.addWidget(self.teams[i][j])
            self.verticalLayout.addLayout(horizontal_layout)

        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)
