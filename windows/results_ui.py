from PyQt5 import QtCore, QtWidgets


class ResultsDialog(object):
    def __init__(self, dialog):
        dialog.resize(400, 412)
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(100, 350, 201, 80))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Copy_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Copy_Button)
        self.Exit_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Exit_Button)
        self.Errors = QtWidgets.QTextBrowser(dialog)
        self.Errors.setGeometry(QtCore.QRect(10, 230, 381, 111))
        self.Text = QtWidgets.QTextBrowser(dialog)
        self.Text.setGeometry(QtCore.QRect(10, 10, 381, 201))
        self.Copied_Label = QtWidgets.QLabel(dialog)
        self.Copied_Label.setEnabled(True)
        self.Copied_Label.setGeometry(QtCore.QRect(14, 350, 371, 20))
        self.Copied_Label.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Copy_Button.setText(_translate("Dialog", "Копировать"))
        self.Exit_Button.setText(_translate("Dialog", "Выход"))
