from PyQt5 import QtCore, QtWidgets

from modules.classes import ConfirmDialogUI

width, height = (400, 412)


class ResultsUI(ConfirmDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна результатов

        :param dialog: окно результатов
        """
        super().__init__(dialog)
        dialog.resize(width, height)
        self.Errors = QtWidgets.QTextBrowser(dialog)
        self.Text = QtWidgets.QTextBrowser(dialog)
        self.Copied_Label = QtWidgets.QLabel(dialog)
        self.Copied_Label.setEnabled(True)
        self.Copied_Label.setAlignment(QtCore.Qt.AlignCenter)

        self.set_size()
        self.Choose_Button.setText("Копировать")
        self.Cancel_Button.setText("Выход")

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.button_widget.setGeometry(QtCore.QRect(int(100 * width/400), int(350 * height/412),
                                                             int(201 * width/400), int(80 * height/412)))
        self.Errors.setGeometry(QtCore.QRect(int(10 * width/400), int(230 * height/412),
                                             int(381 * width/400), int(111 * height/412)))
        self.Text.setGeometry(QtCore.QRect(int(10 * width/400), int(10 * height/412),
                                           int(381 * width/400), int(201 * height/412)))
        self.Copied_Label.setGeometry(QtCore.QRect(int(14 * width/400), int(350 * height/412),
                                                   int(371 * width/400), int(20 * height/412)))
