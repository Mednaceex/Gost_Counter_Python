from PyQt5 import QtCore, QtWidgets


class Line(QtWidgets.QWidget):
    def __init__(self, parent, widget: QtWidgets.QWidget, hint=False, hint_widget=None):
        super(Line, self).__init__()
        self.label = QtWidgets.QLabel(parent)
        self.widget = widget
        self.hint_label = QtWidgets.QLabel(parent) if hint else None
        self.hint_widget = hint_widget

    def align(self, x_label, x_widget, y, widget_width, height):
        self.label.setGeometry(x_label, y, x_widget - x_label, height)
        self.widget.setGeometry(x_widget, y, widget_width, height)
        if self.hint_label is not None:
            self.hint_label.setGeometry(x_label, y + height, x_widget - x_label, 2 * height)
        if self.hint_widget is not None:
            self.hint_widget.setGeometry(x_widget, y + height, widget_width, 2 * height)
