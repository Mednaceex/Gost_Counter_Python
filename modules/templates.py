from PyQt5 import QtCore, QtWidgets


class Line(QtWidgets.QWidget):
    def __init__(self, parent, widget: QtWidgets.QWidget, hint=False, hint_widget=None):
        """
        Конструктор класса строк в меню настроек с подписью, виджетом и подсказкой

        :param parent: родительский виджет PyQT5
        :param widget: виджет, отображаемый в данной строке
        :param hint: наличие или отсутствие подсказки
        :param hint_widget: виджет подсказки (при наличии)
        """
        super().__init__()
        self.label = QtWidgets.QLabel(parent)
        self.widget = widget
        self.hint_label = QtWidgets.QLabel(parent) if hint else None
        self.hint_widget = hint_widget

    def align(self, x_label: int, x_widget: int, y: int, widget_width: int, height: int):
        """
        Устанавливает нужную геометрию строки внутри родительского виджета

        :param x_label: левая координата начала подписи по горизонтали
        :param x_widget: левая координата виджета строки по горизонтали
        :param y: координата строки по вертикали
        :param widget_width: ширина основного виджета
        :param height: высота строки
        """
        self.label.setGeometry(x_label, y, x_widget - x_label, height)
        self.widget.setGeometry(x_widget, y, widget_width, height)
        if self.hint_label is not None:
            self.hint_label.setGeometry(x_label, y + height, x_widget - x_label, 2 * height)
        if self.hint_widget is not None:
            self.hint_widget.setGeometry(x_widget, y + height, widget_width, 2 * height)


class LeagueLine(QtWidgets.QGroupBox):
    def __init__(self, parent, league_name):
        """
        Конструктор строки в меню настройки лиг

        :param parent: родительский виджет PyQT5
        :param league_name: название лиги
        """
        super().__init__()
        self.setParent(parent)
        self.league_name = league_name

        self.buttonwidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.buttonwidget)
        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.league_name)
        self.Choose_Button = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.Choose_Button)
        self.Rename_Button = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.Rename_Button)
        self.Delete_Button = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.Delete_Button)

        self._translate = QtCore.QCoreApplication.translate
        self.Choose_Button.setText(self._translate("Dialog", "Выбрать"))
        self.Rename_Button.setText(self._translate("Dialog", "Переименовать"))
        self.Delete_Button.setText(self._translate("Dialog", "Удалить"))

    def align(self, x_line: int, x_buttons: int, y: int, buttons_width: int, height: int, gap: int):
        """
        Устанавливает нужную геометрию строки внутри родительского виджета

        :param x_line: левая координата начала строки по горизонтали
        :param x_buttons: левая координата левой кнопки по горизонтали
        :param y: координата строки по вертикали
        :param buttons_width: суммарная ширина кнопок
        :param height: высота строки
        :param gap: отступ от начала строки до начала подписи с названием лиги
        """
        self.setGeometry(x_line, y, x_buttons + buttons_width - x_line, height)
        self.label.setGeometry(gap, 0, x_buttons - x_line - gap, height)
        self.buttonwidget.setGeometry(x_buttons - x_line, 0, buttons_width, height)


class Box(QtWidgets.QWidget):
    def __init__(self, width: int, height: int, match_count: int, has_additional: bool):
        """
        Конструктор окна для ввода гостов
        :param width: ширина виджета
        :param height: высота виджета с учётом галочек
        :param match_count: количество матчей в госте (галочек)
        :param has_additional: наличие дополнительной ставки
        """
        super().__init__()
        self.setGeometry(QtCore.QRect(0, 0, int(560 * width/1204), int(287 * height/881)))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.name = QtWidgets.QLabel(self)
        self.verticalLayout.addWidget(self.name)
        self.text = QtWidgets.QTextEdit(self)
        self.text.setStyleSheet("border: 1px solid gray")
        self.verticalLayout.addWidget(self.text)
        checks_layout = QtWidgets.QHBoxLayout()
        checks_layout.setContentsMargins(-1, -1, -1, 0)
        self.labels = []
        self.checks = []
        for j in range(match_count):
            check_layout = QtWidgets.QVBoxLayout()
            check_layout.setContentsMargins(-1, -1, 0, 0)
            self.labels.append(QtWidgets.QLabel(self))
            check_layout.addWidget(self.labels[j], 0, QtCore.Qt.AlignHCenter)
            self.checks.append(QtWidgets.QCheckBox(self))
            self.checks[j].setText("")
            check_layout.addWidget(self.checks[j], 0, QtCore.Qt.AlignHCenter)
            checks_layout.addLayout(check_layout)
        self.verticalLayout.addLayout(checks_layout)

        if has_additional:
            self.add_yes = QtWidgets.QCheckBox(self)
            self.add_no = QtWidgets.QCheckBox(self)
            self.add_yes_label = QtWidgets.QLabel(self)
            self.add_no_label = QtWidgets.QLabel(self)
            self.add_label = QtWidgets.QLabel(self)

            additional_bet_layout = QtWidgets.QVBoxLayout()
            additional_yes_layout = QtWidgets.QHBoxLayout()
            additional_no_layout = QtWidgets.QHBoxLayout()
            additional_yes_layout.addWidget(self.add_yes_label, 0, QtCore.Qt.AlignHCenter)
            additional_yes_layout.addWidget(self.add_yes, 0, QtCore.Qt.AlignHCenter)
            additional_no_layout.addWidget(self.add_no_label, 0, QtCore.Qt.AlignHCenter)
            additional_no_layout.addWidget(self.add_no, 0, QtCore.Qt.AlignHCenter)
            additional_bet_layout.addWidget(self.add_label, 0, QtCore.Qt.AlignHCenter)
            additional_bet_layout.addLayout(additional_yes_layout)
            additional_bet_layout.addLayout(additional_no_layout)
            checks_layout.addLayout(additional_bet_layout)

            self.add_yes.clicked.connect(self.clear_additional_no)
            self.add_no.clicked.connect(self.clear_additional_yes)

    def clear_additional_yes(self):
        """
        Снимает галочку "Да" в окошке дополнительной ставки
        """
        self.add_yes.setCheckState(QtCore.Qt.Unchecked)

    def clear_additional_no(self):
        """
        Снимает галочку "Нет" в окошке дополнительной ставки
        """
        self.add_no.setCheckState(QtCore.Qt.Unchecked)

