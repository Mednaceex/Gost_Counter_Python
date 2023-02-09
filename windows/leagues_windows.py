from PyQt5 import QtWidgets, QtCore

from modules.classes import Dialog, ConfirmDialogUI
from modules.custom_config import get_leagues, save_leagues, get_current_league, save_current_league,\
    set_default_settings, init_files
from modules.text_functions import check_ascii_russian, change_space_to_underscore
from modules.paths import rename_folder, delete_league_folder, init_league
(width, height) = (410, 150)


class LeagueDialog(Dialog):
    def __init__(self, leagues_dialog):
        """
        Конструктор класса окна работы с конкретной лигой

        :param leagues_dialog: окно настройки и выбора лиги
        """
        super().__init__()
        self.leagues_dialog = leagues_dialog
        self.ui = LeagueDialogUI(self)
        self.league_name = 'default'

    def connect_buttons(self):
        self.ui.Cancel_Button.clicked.connect(self.cancel)
        self.ui.Choose_Button.clicked.connect(self.save)

    def open_(self, league_name: str):
        """
        Открывает окно работы с лигой без сообщений об ошибках
        :param league_name: название лиги
        """
        self.ui.set_name(league_name)
        self.show_on_top()
        self.league_name = league_name
        self.ui.error_label.hide()

    def check_new_name(self, new_name: str, league_list: list[str]) -> bool:
        """
        Проверяет наличие ошибки во введённом названии лиги, в случае наличия выводит на экран сообщение о ней
        :param new_name: новое название лиги
        :param league_list: список из названий текущих лиг
        :return: правильность нового названия лиги (булева переменная)
        """
        if new_name in league_list:
            self.set_error("Ошибка: лига с таким названием уже существует")
            return False
        if new_name == "":
            self.set_error("Ошибка: название лиги не может быть пустым")
            return False
        self.hide_error()
        return True

    def set_error(self, text: str):
        """
        Отображает сообщение об ошибке и устанавливает нужный текст

        :param text: текст сообщения
        """
        self.ui.error_label.show()
        self.ui.error_label.setText(text)

    def hide_error(self):
        """
        Скрывает сообщение об ошибке
        """
        self.ui.error_label.hide()

    def cancel(self):
        """
        Закрывает окно и очищает поле ввода
        """
        self.ui.text_field.setText("")
        self.close()

    def save(self):
        pass


class DeleteDialog(LeagueDialog):
    def __init__(self, leagues_dialog):
        """
        Конструктор класса окна удаления лиги

        :param leagues_dialog: окно настройки и выбора лиги
        """
        super().__init__(leagues_dialog)
        self.setWindowTitle("Удаление лиги")
        self.ui = DeleteDialogUI(self)
        self.connect_buttons()

    def save(self):
        """
        Удаляет лигу, удаляет папку лиги, обновляет окно настройки лиг
        """
        delete_league_folder(change_space_to_underscore(self.league_name))
        lst = list(filter(lambda x: x != self.league_name, get_leagues()))
        save_leagues(lst)
        self.leagues_dialog.set_data()
        self.close()


class RenameDialog(LeagueDialog):
    def __init__(self, leagues_dialog):
        """
        Конструктор класса окна переименования лиги

        :param leagues_dialog: окно настройки и выбора лиги
        """
        super().__init__(leagues_dialog)
        self.setWindowTitle("Переименование лиги")
        self.ui = RenameDialogUI(self)
        self.connect_buttons()

    def save(self):
        """
        Переименовывает лигу или выводит сообщение об ошибке
        В случае успешного создания закрывает окно, сохраняет данные о переименованной лиге,
        переименовывает папку лиги
        Обновляет окно настройки лиг, обновляет названия лиг у объектов главного окна
        """
        league_list = get_leagues()
        text = change_space_to_underscore(check_ascii_russian(self.ui.text_field.text()))
        if not self.check_new_name(text, league_list):
            return
        lst = [text if league == self.league_name else league for league in league_list]
        save_leagues(lst)
        rename_folder(change_space_to_underscore(self.league_name), text)
        if get_current_league() == self.league_name:
            save_current_league(text)
        self.leagues_dialog.set_data()
        self.leagues_dialog.main_window.update_betters_league(self.league_name, text)
        self.cancel()


class LeagueDialogUI(ConfirmDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна работы с конкретной лигой

        :param dialog: окно работы с конкретной лигой
        """
        super().__init__(dialog)

    def set_name(self, league_name: str):
        """
        Устанавливает название лиги и выводимое сообщение
        :param league_name: название лиги
        """
        pass


class DeleteDialogUI(LeagueDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна удаления лиги

        :param dialog: окно удаления лиги
        """
        super().__init__(dialog)
        dialog.resize(width, height)

        self.set_size()
        self.set_standard_buttons()

    def set_name(self, league_name: str):
        """
        Устанавливает название лиги и выводимое сообщение
        :param league_name: название лиги
        """
        self.label.setText(f'\"{league_name}\"  будет безвозвратно удалена.')

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.label.setGeometry(
            int(10 * width / 410), int(30 * height / 200), int(390 * width / 410), int(80 * height / 200))
        self.button_widget.setGeometry(QtCore.QRect(int(50 * width/350), int(120 * height/200),
                                                             int(250 * width/350), int(60 * height/200)))


class RenameDialogUI(LeagueDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна переименования лиги

        :param dialog: окно переименования лиги
        """
        super().__init__(dialog)
        dialog.resize(width, height)
        self.text_field.show()
        self.text_field.setText("")

        self.set_size()
        self.set_standard_buttons()

    def set_name(self, league_name: str):
        """
        Устанавливает название лиги и выводимое сообщение
        :param league_name: название лиги
        """
        self.label.setText(f'Введите новое название лиги \"{league_name}\":')

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.text_field.setGeometry(
            int(20 * width / 410), int(70 * height / 200), int(370 * width / 410), int(30 * height / 200))
        self.error_label.setGeometry(
            int(20 * width / 410), int(102 * height / 200), int(370 * width / 410), int(30 * height / 200))
        self.button_widget.setGeometry(QtCore.QRect(int(80 * width / 410), int(120 * height / 200),
                                                             int(250 * width / 410), int(60 * height / 200)))
        self.label.setGeometry(
            int(10 * width / 410), int(20 * height / 200), int(390 * width / 410), int(40 * height / 200))


class AddLeague(LeagueDialog):
    def __init__(self, leagues_dialog):
        """
        Конструктор класса окна добавления лиги

        :param leagues_dialog: окно настройки и выбора лиги
        """
        super().__init__(leagues_dialog)
        self.ui = AddLeagueUI(self)
        self.leagues_dialog = leagues_dialog
        self.setWindowTitle("Добавление новой лиги")
        self.connect_buttons()

    def save(self):
        """
        Создаёт новую лигу или выводит сообщение об ошибке
        В случае успешного создания закрывает окно, сохраняет данные о добавленной лиге,
        создаёт папку лиги и инициализирует нужные файлы
        Обновляет окно настройки лиг
        """
        league_list = get_leagues()
        text = change_space_to_underscore(check_ascii_russian(self.ui.text_field.text()))
        if not self.check_new_name(text, league_list):
            return
        init_league(text)
        set_default_settings(text)
        init_files(text)
        league_list.append(text)
        save_leagues(league_list)
        self.leagues_dialog.set_data()
        self.cancel()


class AddLeagueUI(ConfirmDialogUI):
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса окна добавления лиги

        :param dialog: окно добавления лиги
        """
        super().__init__(dialog)
        dialog.resize(width, height)
        self.text_field = QtWidgets.QLineEdit(dialog)

        self.set_size()
        self.label.setText("Введите название новой лиги:")
        self.text_field.setText("")
        self.Choose_Button.setText("Добавить")
        self.Cancel_Button.setText("Отмена")

    def set_size(self):
        """
        Задаёт нужную геометрию окна
        """
        self.label.setGeometry(
            int(10 * width / 410), int(20 * height / 200), int(390 * width / 410), int(40 * height / 200))
        self.button_widget.setGeometry(QtCore.QRect(int(80 * width/410), int(120 * height/200),
                                                             int(250 * width/410), int(60 * height/200)))
        self.text_field.setGeometry(
            int(20 * width / 410), int(70 * height / 200), int(370 * width / 410), int(30 * height / 200))
        self.error_label.setGeometry(
            int(20 * width / 410), int(102 * height / 200), int(370 * width / 410), int(30 * height / 200))
