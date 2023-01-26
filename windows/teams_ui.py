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
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(int(10 * width/756), 0,
                                                int(721 * width/756), int(742 * height * get_player_count()/15820)))
        self.spacing_layout = QtWidgets.QVBoxLayout()
        self.spacing_layout.setContentsMargins(-1, -1, -1, 0)
        self.spacing_layout.setSpacing(int(8 * height/791))
        size_policy_preferred = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy_preferred.setHorizontalStretch(0)
        size_policy_preferred.setVerticalStretch(0)
        for i in range(2):
            label = QtWidgets.QLabel(self.horizontalLayoutWidget)
            size_policy_preferred.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(size_policy_preferred)
            label.setText("")
            self.spacing_layout.addWidget(label)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        self.vertical_layout.setContentsMargins(-1, -1, -1, 0)
        self.vertical_layout.setSpacing(int(10 * height/791))
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.setContentsMargins(-1, -1, -1, 0)
        self.title_layout.setSpacing(0)
        self.label_team_name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.title_layout.addWidget(self.label_team_name, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label_coach_name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.title_layout.addWidget(self.label_coach_name, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vertical_layout.addLayout(self.title_layout)
        self.label = []
        self.teams = []
        self.names = []
        for i in range(get_player_count()):
            horizontal_layout = QtWidgets.QHBoxLayout()
            self.label.append(QtWidgets.QLabel(self.horizontalLayoutWidget))
            self.label[i].setFixedWidth(20)
            for line_list in (self.teams, self.names):
                line_list.append(QtWidgets.QLineEdit(self.horizontalLayoutWidget))
                horizontal_layout.addWidget(self.label[i])
                horizontal_layout.addWidget(line_list[i])
            self.vertical_layout.addLayout(horizontal_layout)

        self.retranslate_ui()
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        for i in range(get_player_count()):
            self.label[i].setText(_translate("Dialog", f"{i + 1}."))
        self.label_team_name.setText(_translate("Dialog", "Название команды"))
        self.label_coach_name.setText(_translate("Dialog", "Тренер"))
