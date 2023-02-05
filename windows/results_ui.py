from PyQt5 import QtCore, QtWidgets
width, height = (400, 412)


class ResultsDialog:
    def __init__(self, dialog):
        dialog.resize(width, height)
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(int(100 * width/400), int(350 * height/412),
                                                             int(201 * width/400), int(80 * height/412)))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Copy_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Copy_Button)
        self.Exit_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Exit_Button)
        self.Errors = QtWidgets.QTextBrowser(dialog)
        self.Errors.setGeometry(QtCore.QRect(int(10 * width/400), int(230 * height/412),
                                             int(381 * width/400), int(111 * height/412)))
        self.Text = QtWidgets.QTextBrowser(dialog)
        self.Text.setGeometry(QtCore.QRect(int(10 * width/400), int(10 * height/412),
                                           int(381 * width/400), int(201 * height/412)))
        self.Copied_Label = QtWidgets.QLabel(dialog)
        self.Copied_Label.setEnabled(True)
        self.Copied_Label.setGeometry(QtCore.QRect(int(14 * width/400), int(350 * height/412),
                                                   int(371 * width/400), int(20 * height/412)))
        self.Copied_Label.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Copy_Button.setText(_translate("Dialog", "Копировать"))
        self.Exit_Button.setText(_translate("Dialog", "Выход"))
