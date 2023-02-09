from PyQt5 import QtCore, QtWidgets
from modules.templates import Line
from modules.classes import ConfirmDialogUI

width, height = (924, 667)
(x_label, x_widget, y, widget_width, line_height, gap) =\
    map(int, (10 * width/924, 345 * width/924, 15 * height/667,
              555 * width/924, 20 * height/667, 20 * height/667))


class SettingsUI(ConfirmDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна настроек

        :param dialog: окно настроек
        """
        super().__init__(dialog)
        dialog.resize(width, height)
        self.central_widget = QtWidgets.QWidget(dialog)

        self.player_count = Line(self.central_widget, QtWidgets.QLineEdit(self.central_widget))
        self.match_count = Line(self.central_widget, QtWidgets.QLineEdit(self.central_widget))
        self.has_additional = Line(self.central_widget, QtWidgets.QCheckBox(self.central_widget))
        # self.auto_update = Line(self.central_widget, QtWidgets.QCheckBox(self.central_widget),
        # True, QtWidgets.QPushButton(self.central_widget))

        self.set_size()
        self.set_standard_buttons()
        self.player_count.label.setText("Количество игроков")
        self.match_count.label.setText("Количество матчей в госте")
        self.has_additional.label.setText("Дополнительная ставка")
        # self.auto_update.label.setText("Автоматическая проверка обновлений (в разработке)")
        # self.auto_update.hint_label.setText("При отключении этой опции вы сможете\n"
        # "проверить наличие обновлений здесь: (в разработке)")
        # self.auto_update.hint_widget.setText("Проверить обновления")

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.central_widget.setGeometry(QtCore.QRect(int(10 * width/924), int(10 * height/667),
                                                     int(901 * width/924), int(530 * height/667)))
        self.button_widget.setGeometry(QtCore.QRect(int(310 * width/924), int(540 * height/667),
                                                    int(281 * width/924), int(52 * height/667)))
        for index, line in enumerate((self.player_count, self.match_count, self.has_additional  # , self.auto_update
                                      )):
            line.align(x_label, x_widget, y + (line_height + gap) * index, widget_width, line_height)
