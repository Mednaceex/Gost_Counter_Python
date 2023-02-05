from PyQt5 import QtCore, QtWidgets
from modules.templates import Line

width, height = (924, 667)
(x1, x2, y, ww, h, gap) =\
    (10 * width/924, 345 * width/924, 15 * height/667, 555 * width/924, 20 * height/667, 20 * height/667)


class SettingsDialog:
    def __init__(self, dialog):
        dialog.resize(width, height)
        self.central_widget = QtWidgets.QWidget(dialog)
        self.central_widget.setGeometry(QtCore.QRect(int(10 * width/924), int(10 * height/667),
                                                     int(901 * width/924), int(650 * height/667)))
        self.buttonBox = QtWidgets.QDialogButtonBox(self.central_widget)
        self.buttonBox.setGeometry(QtCore.QRect(int(350 * width/924), int(560 * height/667),
                                                int(201 * width/924), int(32 * height/667)))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.player_count = Line(self.central_widget, QtWidgets.QLineEdit(self.central_widget))
        self.match_count = Line(self.central_widget, QtWidgets.QLineEdit(self.central_widget))
        self.has_additional = Line(self.central_widget, QtWidgets.QCheckBox(self.central_widget))
        # self.auto_update = Line(self.central_widget, QtWidgets.QCheckBox(self.central_widget),
        # True, QtWidgets.QPushButton(self.central_widget))
        for index, line in enumerate((self.player_count, self.match_count, self.has_additional,  # self.auto_update
                                      )):
            line.align(x1, x2, y + (h + gap) * index, ww, h)

        self.retranslate_ui()
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.player_count.label.setText(_translate("Dialog", "Количество игроков"))
        self.match_count.label.setText(_translate("Dialog", "Количество матчей в госте"))
        self.has_additional.label.setText(_translate("Dialog", "Дополнительная ставка"))
        # self.auto_update.label.setText(_translate("Dialog", "Автоматическая проверка обновлений (в разработке)"))
        # self.auto_update.hint_label.setText(_translate("Dialog", "При отключении этой опции вы сможете\n"
        # "проверить наличие обновлений здесь: (в разработке)"))
        # self.auto_update.hint_widget.setText(_translate("Dialog", "Проверить обновления"))
