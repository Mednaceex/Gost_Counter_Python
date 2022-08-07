from PyQt5 import QtWidgets, QtCore

from modules.paths import players_txt
from modules.text_functions import split
from modules.custom_config import match_count


class Better:
    def __init__(self, name: str, goals=[0] * match_count):
        """
        Конструктор класса игроков

        :param name: название команды игрока
        :param goals: список количества голов, забитых игроком на каждой ставке
        """
        self.name = name
        self.player_name = self.get_name()
        self.goals = goals

    def set_goals(self, value):
        """
        Изменяет количество голов игрока на заданное параметром value
        """
        self.goals = value

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
