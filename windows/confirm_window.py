from PyQt5 import QtWidgets, QtCore

from modules.classes import Dialog, League
from windows.results_ui import ResultsDialog
from modules.custom_config import get_leagues, save_leagues, get_current_league, set_current_league,\
    set_default_settings, init_files
from modules.text_functions import check_ascii_russian, change_space_to_underscore
from modules.paths import rename_folder, delete_league_folder, init_league
(width, height) = (410, 150)


class ConfirmWindow(Dialog):
    def __init__(self, leagues_dialog):
        """
        Конструктор класса окна с итогами матчей

        :param leagues_dialog: окно настройки и выбора лиги
        """
        super().__init__()
        self.leagues_dialog = leagues_dialog
        self.ui = ConfirmWindowDialog(self)
        self.league_name = 'default'

    def open_(self, league_name: str):
        self.ui.set_name(league_name)
        self.show_on_top()
        self.league_name = league_name
        self.ui.error_label.hide()


class DeleteConfirmWindow(ConfirmWindow):
    def __init__(self, leagues_dialog):
        super().__init__(leagues_dialog)
        self.setWindowTitle("Удаление лиги")
        self.ui = DeleteConfirmWindowDialog(self)
        self.ui.Cancel_Button.clicked.connect(self.close)
        self.ui.Choose_Button.clicked.connect(self.save)

    def save(self):
        delete_league_folder(change_space_to_underscore(self.league_name))
        lst = list(filter(lambda x: x != self.league_name, get_leagues()))
        save_leagues(lst)
        self.leagues_dialog.set_data()
        self.close()


class RenameConfirmWindow(ConfirmWindow):
    def __init__(self, leagues_dialog):
        super().__init__(leagues_dialog)
        self.setWindowTitle("Переименование лиги")
        self.ui = RenameConfirmWindowDialog(self)
        self.ui.Choose_Button.clicked.connect(self.save)
        self.ui.Cancel_Button.clicked.connect(self.cancel)

    def save(self):
        league_list = get_leagues()
        text = change_space_to_underscore(check_ascii_russian(self.ui.text_field.text()))
        if text in league_list:
            self.set_error("Ошибка: лига с таким названием уже существует")
            return
        if text == "":
            self.set_error("Ошибка: название лиги не может быть пустым")
            return
        self.hide_error()
        for i, league in enumerate(league_list):
            if league == self.league_name:
                league_list[i] = text
                break
        save_leagues(league_list)
        rename_folder(change_space_to_underscore(self.league_name), text)
        if get_current_league() == self.league_name:
            set_current_league(text)
        self.leagues_dialog.set_data()
        self.ui.text_field.setText("")
        self.leagues_dialog.main_window.update_betters_league(self.league_name, text)
        self.close()

    def set_error(self, text: str):
        self.ui.error_label.show()
        self.ui.error_label.setText(text)

    def hide_error(self):
        self.ui.error_label.hide()

    def cancel(self):
        self.ui.text_field.setText("")
        self.close()


class ConfirmWindowDialog:
    def __init__(self, dialog):
        self.error_label = QtWidgets.QLabel(dialog)

    def set_name(self, league_name: str):
        pass


class DeleteConfirmWindowDialog(ConfirmWindowDialog):
    def __init__(self, dialog):
        super().__init__(dialog)
        dialog.resize(width, height)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(
            int(10 * width / 410), int(30 * height / 200), int(390 * width / 410), int(80 * height / 200))
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(int(50 * width/350), int(120 * height/200),
                                                             int(250 * width/350), int(60 * height/200)))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Choose_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Choose_Button)
        self.Cancel_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Cancel_Button)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Choose_Button.setText(_translate("Dialog", "Ок"))
        self.Cancel_Button.setText(_translate("Dialog", "Отмена"))

    def set_name(self, league_name: str):
        self.label.setText(f'\"{league_name}\"  будет безвозвратно удалена.')


class RenameConfirmWindowDialog(ConfirmWindowDialog):
    def __init__(self, dialog):
        super().__init__(dialog)
        dialog.resize(width, height)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(
            int(10 * width / 410), int(20 * height / 200), int(390 * width / 410), int(40 * height / 200))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(int(80 * width/410), int(120 * height/200),
                                                             int(250 * width/410), int(60 * height/200)))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Choose_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Choose_Button)
        self.Cancel_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Cancel_Button)

        self.text_field = QtWidgets.QLineEdit(dialog)
        self.text_field.setText("")
        self.text_field.setGeometry(
            int(20 * width / 410), int(70 * height / 200), int(370 * width / 410), int(30 * height / 200))

        self.error_label = QtWidgets.QLabel(dialog)
        self.error_label.setGeometry(
            int(20 * width / 410), int(102 * height / 200), int(370 * width / 410), int(30 * height / 200))
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Choose_Button.setText(_translate("Dialog", "Ок"))
        self.Cancel_Button.setText(_translate("Dialog", "Отмена"))

    def set_name(self, league_name: str):
        self.label.setText(f'Введите новое название лиги \"{league_name}\":')


class AddLeague(Dialog):
    def __init__(self, leagues_dialog):
        super().__init__()
        self.ui = AddLeagueDialog(self)
        self.leagues_dialog = leagues_dialog
        self.setWindowTitle("Добавление новой лиги")
        self.ui.Ok_Button.clicked.connect(self.save)
        self.ui.Cancel_Button.clicked.connect(self.cancel)

    def cancel(self):
        self.ui.text_field.setText("")
        self.close()

    def save(self):
        league_list = get_leagues()
        text = change_space_to_underscore(check_ascii_russian(self.ui.text_field.text()))
        if text in league_list:
            self.set_error("Ошибка: лига с таким названием уже существует")
            return
        if text == "":
            self.set_error("Ошибка: название лиги не может быть пустым")
            return
        self.hide_error()
        init_league(text)
        set_default_settings(text)
        init_files(text)
        league_list.append(text)
        save_leagues(league_list)
        self.leagues_dialog.set_data()
        self.ui.text_field.setText("")
        self.close()

    def set_error(self, text: str):
        self.ui.error_label.show()
        self.ui.error_label.setText(text)

    def hide_error(self):
        self.ui.error_label.hide()


class AddLeagueDialog:
    def __init__(self, dialog):
        super().__init__()
        dialog.resize(width, height)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(
            int(10 * width / 410), int(20 * height / 200), int(390 * width / 410), int(40 * height / 200))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Введите название новой лиги:")
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(int(80 * width/410), int(120 * height/200),
                                                             int(250 * width/410), int(60 * height/200)))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Ok_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Ok_Button)
        self.Cancel_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.Cancel_Button)

        self.text_field = QtWidgets.QLineEdit(dialog)
        self.text_field.setText("")
        self.text_field.setGeometry(
            int(20 * width / 410), int(70 * height / 200), int(370 * width / 410), int(30 * height / 200))
        self.error_label = QtWidgets.QLabel(dialog)
        self.error_label.setGeometry(
            int(20 * width / 410), int(102 * height / 200), int(370 * width / 410), int(30 * height / 200))
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Ok_Button.setText(_translate("Dialog", "Добавить"))
        self.Cancel_Button.setText(_translate("Dialog", "Отмена"))
