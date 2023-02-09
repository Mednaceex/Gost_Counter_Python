from PyQt5 import QtWidgets, QtCore

from modules.paths import get_path
from modules.text_functions import split, change_space_to_underscore, change_underscore_to_space, get_data


class League:
    def __init__(self, league_name, folder_name=None):
        """
        Конструктор класса лиг

        :param league_name: название лиги
        :param folder_name: название папки, в которой хранятся данные лиги
        (при отсутствии параметра идентично названию лиги)
        """
        self.name = change_underscore_to_space(league_name)
        self.folder_name = change_space_to_underscore(league_name) if folder_name is None else folder_name

    def get_custom_data(self):
        """
        Находит пользовательские настройки в файле

        :return: Словарь значений
        """
        with open(self.get_custom_txt(), 'r') as custom:
            text = custom.readlines()
        d = {}
        for line in text:
            lst = split(line, '=')
            (param, value) = lst
            d[param] = value
        return d

    def get_int_data(self, setting: str):
        """
        Находит пользовательское значение настройки, имеющей целочисленное значение, в файле

        :param setting: название настройки
        :return: значение настройки
        """
        with open(self.get_custom_txt(), 'r') as custom:
            text = custom.readlines()
        return int(get_data(text, setting))

    def get_bool_data(self, setting: str):
        """
        Находит пользовательское значение настройки, имеющей только булевы значения, в файле

        :param setting: название настройки
        :return: булева переменная
        """
        with open(self.get_custom_txt(), 'r') as custom:
            text = custom.readlines()
        return get_data(text, setting) == "True"

    def get_has_additional(self):
        """
        Находит пользовательское значение настройки наличия дополнительной ставки в файле

        :return: булева переменная - наличие дополнительной ставки
        """
        return self.get_bool_data('has_additional')

    def get_player_count(self):
        """
        Находит пользовательское значение количества игроков в файле

        :return: количество игроков
        """
        return self.get_int_data('player_count')

    def get_match_count(self):
        """
        Находит пользовательское значение количества матчей в файле

        :return: количество матчей
        """
        return self.get_int_data('match_count')

    def get_auto_update(self):
        """
        Находит пользовательское значение настройки автообновлений в файле

        :return: булева переменная - наличие автоообновлений
        """
        return self.get_bool_data('auto_update')

    def get_saved_txt(self):
        return get_path(self.folder_name, 'saved.txt')

    def get_errors_txt(self):
        return get_path(self.folder_name, 'errors.txt')

    def get_checks_txt(self):
        return get_path(self.folder_name, 'checks.txt')

    def get_scores_txt(self):
        return get_path(self.folder_name, 'scores.txt')

    def get_matches_txt(self):
        return get_path(self.folder_name, 'matches.txt')

    def get_output_txt(self):
        return get_path(self.folder_name, 'output.txt')

    def get_custom_txt(self):
        return get_path(self.folder_name, 'custom.txt')

    def get_additional_txt(self):
        return get_path(self.folder_name, 'additional.txt')

    def get_players_txt(self):
        return get_path(self.folder_name, 'players.txt')


class Result:
    def __init__(self, valid: bool):
        """
        Конструктор класса результатов ставки

        :param valid: определяет, имеется ли ставка в наличии
        """
        self.valid = valid
        self.result = False  # угаданный исход матча
        self.diff = False  # угаданная разница голов
        self.exact = False  # угаданный точный счёт
        self.winner = False  # угаданный исход дополнительной ставки


class BetResult(Result):
    def __init__(self, winner: bool, diff: bool, exact: bool):
        """
        Конструктор класса результатов ставки

        :param winner: угаданный исход матча
        :param diff: угаданная разница голов
        :param exact: угаданный точный счёт
        """
        super().__init__(valid=True)
        self.winner = winner
        self.diff = diff
        self.exact = exact


class AddBetResult(Result):
    def __init__(self, result: bool):
        """
        Конструктор класса результатов дополнительной ставки

        :param result: угаданный исход дополнительной ставки
        """
        super().__init__(valid=True)
        self.result = result


class Better:
    def __init__(self, league: League, name: str, results=None):
        """
        Конструктор класса игроков

        :param league: название лиги игрока
        :param name: название команды игрока
        :param results: список результатов каждой ставки (объектов класса BetResult)
        """
        self.name = name
        self.league = league
        self.player_name = self.get_name()
        if results is None:  # задаёт стандартное значение результатов игрока - ничего не угадано
            self.results = [Result(valid=False)] * (self.league.get_match_count()+int(self.league.get_has_additional()))
        else:
            self.results = results

    def set_results(self, value):
        """
        Изменяет количество голов игрока на заданное параметром value
        """
        self.results = value

    def get_name(self):
        """
        Считывает имя игрока из файла

        :return: имя игрока (строка)
        """
        with open(self.league.get_players_txt(), 'r') as players:
            text = players.readlines()
        return get_data(text, self.name, ' - ')


class BetText:
    def __init__(self, better: Better, text: str, number: int):
        """
        Конструктор класса строк с текстом госта, присылаемого игроком

        :param better: автор госта
        :param text: текст госта
        :param number: номер окна ввода для данного игрока
        """
        self.better = better
        self.text = text
        self.number = number
        self.name = better.name


class Error:
    def __init__(self, name, number):
        """
        Конструктор класса сообщений о недостаточном числе ставок в госте

        :param name: название команды
        :param number: количество ставок в госте
        """
        self.name = name
        self.number = number


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        """
        Конструктор класса диалоговых окон без значка справки
        """
        super(Dialog, self).__init__()
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

    def show_on_top(self):
        """
        Открывает окно и отображает его поверх остальных окон
        """
        self.show()
        self.raise_()
        self.activateWindow()


class ConfirmDialogUI:
    def __init__(self, dialog):
        """
        Конструктор графического интерфейса диалогового окна с кнопками "Ок" и "Отмена"

        :param dialog: диалоговое окно
        """
        self.label = QtWidgets.QLabel(dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label = QtWidgets.QLabel(dialog)
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_field = QtWidgets.QLineEdit(dialog)
        self.text_field.hide()

        self.button_widget = QtWidgets.QWidget(dialog)
        self.button_layout = QtWidgets.QHBoxLayout(self.button_widget)
        self.button_layout.removeWidget(self.button_widget)
        self.Choose_Button = QtWidgets.QPushButton(self.button_widget)
        self.button_layout.addWidget(self.Choose_Button)
        self.Cancel_Button = QtWidgets.QPushButton(self.button_widget)
        self.button_layout.addWidget(self.Cancel_Button)  # Каким-то магическим образом убирает двоящиеся кнопки

    def set_standard_buttons(self):
        """
        Задаёт названия "Ок" и "Отмена" у кнопок
        """
        self.Choose_Button.setText("Ок")
        self.Cancel_Button.setText("Отмена")


class BetListError(Exception):
    def __init__(self):
        """
        Конструктор класса ошибок, выдающихся при попытке посчитать список ставок при неправильном их количестве
        """
        super().__init__("Неправильное количество матчей в госте")
