from PyQt5 import QtCore, QtWidgets


class Line(QtWidgets.QWidget):
    def __init__(self, parent, widget: QtWidgets.QWidget, hint=False, hint_widget=None):
        super(Line, self).__init__()
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
