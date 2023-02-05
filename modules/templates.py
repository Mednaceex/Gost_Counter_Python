from PyQt5 import QtCore, QtWidgets


class Line(QtWidgets.QWidget):
    def __init__(self, parent, widget: QtWidgets.QWidget, hint=False, hint_widget=None):
        super().__init__()
        self.label = QtWidgets.QLabel(parent)
        self.widget = widget
        self.hint_label = QtWidgets.QLabel(parent) if hint else None
        self.hint_widget = hint_widget

    def align(self, x_label, x_widget, y, widget_width, height):
        self.label.setGeometry(int(x_label), int(y), int(x_widget - x_label), int(height))
        self.widget.setGeometry(int(x_widget), int(y), int(widget_width), int(height))
        if self.hint_label is not None:
            self.hint_label.setGeometry(int(x_label), int(y + height), int(x_widget - x_label), int(2 * height))
        if self.hint_widget is not None:
            self.hint_widget.setGeometry(int(x_widget), int(y + height), int(widget_width), int(2 * height))


class LeagueLine(QtWidgets.QGroupBox):
    def __init__(self, parent, league_name):
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

    def align(self, x_label, x_buttons, y, buttons_width, height, gap):
        self.setGeometry(int(x_label), int(y), int(x_buttons + buttons_width - x_label), int(height))
        self.label.setGeometry(int(gap), int(0), int(x_buttons - x_label), int(height))
        self.buttonwidget.setGeometry(int(x_buttons - x_label), int(0), int(buttons_width), int(height))
