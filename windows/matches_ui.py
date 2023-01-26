from PyQt5 import QtCore, QtWidgets

from modules.custom_config import player_count
from modules.templates import Line
width, height = (924, 667)


class MatchesDialog(object):
    def __init__(self, dialog):
        dialog.resize(width, height)
        self.central_widget = QtWidgets.QWidget()
        self.buttonBox = QtWidgets.QDialogButtonBox(self.central_widget)
        self.buttonBox.setGeometry(QtCore.QRect(int(350 * width/924), int(560 * height/667),
                                                int(201 * width/924), int(32 * height/667)))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(int(20 * width/924),
                                                           int(10 * height/667),
                                                           int(881 * width/924),
                                                           int(481 * height * (player_count/2) / 6670)))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.teams = []
        for i in range(int(player_count / 2)):
            self.teams.append([])
            horizontal_layout = QtWidgets.QHBoxLayout()
            for j in range(2):
                self.teams[i].append(QtWidgets.QComboBox(self.verticalLayoutWidget))
                horizontal_layout.addWidget(self.teams[i][j])
            self.verticalLayout.addLayout(horizontal_layout)

        self.field_factor = Line(self.central_widget, QtWidgets.QCheckBox(self.central_widget))
        self.field_factor.align(32 * width / 924, 160 * width / 924,
                                int((100 + 481 * (player_count/2)) * height / 6670),
                                555 * width / 924, 20 * height / 667)

        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        self.layout = QtWidgets.QGridLayout(dialog)
        self.layout.addWidget(self.central_widget, 0, 0)

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.field_factor.label.setText(_translate("Dialog", "Домашний фактор"))
