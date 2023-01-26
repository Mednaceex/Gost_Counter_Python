from PyQt5 import QtWidgets, QtCore

from modules.paths import players_txt
from modules.text_functions import split
from modules.custom_config import get_match_count, get_has_additional


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
    def __init__(self, name: str, results=[Result(valid=False)] * (get_match_count() + int(get_has_additional()))):
        """
        Конструктор класса игроков

        :param name: название команды игрока
        :param results: список результатов каждой ставки (объектов класса BetResult)
        """
        self.name = name
        self.player_name = self.get_name()
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
        with open(players_txt, 'r') as players:
            text = players.readlines()
        for line in text:
            player = split(line, ' - ')
            if player[0] == self.name:
                name = player[1]
        return name


class BetText:
    def __init__(self, name, text, number):
        """
        Конструктор класса строк с текстом госта, присылаемого игроком

        :param name: название команды
        :param text: текст госта
        :param number: номер окна ввода для данного игрока
        """
        self.name = name
        self.text = text
        self.number = number


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
