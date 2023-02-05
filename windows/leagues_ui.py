from PyQt5 import QtCore, QtWidgets, QtGui
from modules.templates import LeagueLine
from modules.custom_config import get_leagues, get_current_league
width, height = (584, 697)


class LeaguesDialog:
    def __init__(self, dialog):
        self.dialog = dialog
        dialog.resize(width, height)
        self.league_editor_widget = QtWidgets.QScrollArea(dialog)
        self.scroll_area_contents = QtWidgets.QWidget(self.league_editor_widget)
        self.league_editor_widget.setWidget(self.scroll_area_contents)
        self.league_editor_widget.setGeometry(15, 100, 554, 500)
        self.scroll_area_contents.setGeometry(0, 0, 519, 15 + 50 * len(get_leagues()))

        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(int(100 * width/400), int(350 * height/412),
                                                             int(201 * width/400), int(80 * height/412)))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Add_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Add_Button)
        self.Cancel_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Cancel_Button)
        self.league_list = get_leagues()
        self.box_list = []
        self.set_boxes(self.league_list)

        self.current_label = QtWidgets.QLabel(dialog)
        self.current_label.setGeometry(15, 30, 554, 40)
        self.current_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_label.setFont(QtGui.QFont("Arial", 10))
        self.set_current_label(get_current_league())

        self.error_label = QtWidgets.QLabel(dialog)
        self.error_label.setGeometry(15, 608, 554, 30)
        self.error_label.setText("Ошибка: нельзя удалить текущую лигу")
        self.error_label.hide()
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Add_Button.setText(_translate("Dialog", "Добавить лигу"))
        self.Cancel_Button.setText(_translate("Dialog", "Выход"))

    def set_current_label(self, league_name: str):
        self.current_label.setText(f'Текущая лига: {league_name}')

    def set_boxes(self, league_list):
        self.league_list = league_list
        self.box_list = []
        for i, league_name in enumerate(league_list):
            line = LeagueLine(self.scroll_area_contents, league_name)
            line.align(10, 209, 10 + i * 50, 310, 45, 20)
            line.setVisible(True)
            self.box_list.append(line)
        self.scroll_area_contents.setGeometry(0, 0, 519, 15 + 50 * len(league_list))

    def remove_boxes(self):
        for box in reversed(self.box_list):
            box.setParent(None)
