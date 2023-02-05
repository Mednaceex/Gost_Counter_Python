from PyQt5 import QtWidgets, QtCore

from modules.paths import get_path
from modules.text_functions import split, change_space_to_underscore


class League:
    def __init__(self, league_name, folder_name=None):
        """
        Конструктор класса лиг

        :param league_name: название лиги
        :param folder_name: название папки, в которой хранятся данные лиги
        (при отсутствии параметра идентично названию лиги)
        """
        self.name = league_name
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

    def get_int_data(self, txt: str):
        """
        Находит пользовательское значение настройки, имеющей целочисленное значение, в файле

        :param txt: название настройки
        :return: значение настройки
        """
        a = self.get_custom_txt()
        with open(a, 'r') as custom:
            text = custom.readlines()
        for line in text:
            lst = split(line, '=')
            if lst[0] == txt:
                return int(lst[1])

    def get_bool_data(self, txt: str):
        """
        Находит пользовательское значение настройки, имеющей только булевы значения, в файле

        :param txt: название настройки
        :return: булева переменная
        """
        with open(self.get_custom_txt(), 'r') as custom:
            text = custom.readlines()
        for line in text:
            lst = split(line, '=')
            if lst[0] == txt:
                return lst[1] == "True"

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
        self.winner = False
        self.diff = False
        self.exact = False
        self.result = False

    def __repr__(self):
        return str(self.winner) + str(self.diff) + str(self.exact)


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
        if results is None:
            self.results =\
                [Result(valid=False)] * (self.league.get_match_count() + int(self.league.get_has_additional()))
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
        name = ''
        with open(self.league.get_players_txt(), 'r') as players:
            text = players.readlines()
        for line in text:
            player = split(line, ' - ')
            if player[0] == self.name:
                name = player[1]
        return name


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
