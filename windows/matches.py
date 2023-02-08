from PyQt5 import QtCore

from modules.text_functions import split, get_rid_of_slash_n
from modules.classes import Dialog, League
from windows.matches_ui import MatchesUI


class Matches(Dialog):
    def __init__(self, main_window, league: League):
        """
        Конструктор класса окна настройки матчей

        :param league: лига, в которой проходят матчи
        """
        super(Matches, self).__init__()
        self.league = league
        self.main_window = main_window
        self.ui = MatchesUI(self)
        self.config_teams()
        self.set_names()
        self.set_field_factor()
        self.ui.Choose_Button.clicked.connect(self.save)
        self.ui.Cancel_Button.clicked.connect(self.close)
        self.setWindowTitle('Настройка матчей')

    def save(self):
        """
        Сохраняет данные о матчах в файл, закрывает окно
        """
        self.save_matches(self.league.get_matches_txt())
        self.close()

    def save_matches(self, file):
        """
        Сохраняет данные о матчах в файл

        :param file: путь к файлу
        """
        text = 'field_factor='
        text += str(self.ui.field_factor.widget.isChecked())
        for i in range(int(self.league.get_player_count() / 2)):
            name = [''] * 2
            for j in range(2):
                name[j] = self.ui.teams[i][j].currentText()
            text += '\n' + name[0] + ' - ' + name[1]
        with open(file, 'w') as matches:
            print(text, file=matches, end='')

    def check_repeats(self):
        """
        Проверяет наличие повторяющихся команд в настроенном расписании

        :return: True, если повторения есть, False иначе
        """
        self.league = self.main_window.league
        teams = [''] * self.league.get_player_count()
        matches = self.read_matches(self.league)
        for i, line in enumerate(matches):
            if i >= int(self.league.get_player_count() / 2):
                break
            for j in range(2):
                teams[2 * i + j] = matches[i][j]
        return len(set(teams)) != len(teams)  # Проверяет отсутствие повторений в списке

    def read_teams(self):
        """
        Считывает названия команд из файла

        :return: список названий команд
        """
        with open(self.league.get_players_txt(), 'r') as players:
            text = players.readlines()
        names = [split(line, ' - ')[0] for line in text]
        return names

    @staticmethod
    def read_matches(league):
        """
        Считывает матчи из файла

        :param league: лига, в которой проходят матчи
        :return: список матчей (каждый элемент списка - список из двух названий команд)
        """
        with open(league.get_matches_txt(), 'r') as matches:
            text = matches.readlines()
        matches = [split(line, ' - ') for i, line in enumerate(text)]
        return matches[1:]

    @staticmethod
    def read_field_factor(league):
        """
        Считывает данные о факторе домашнего поля из файла

        :param league: лига, в которой проходят матчи
        :return: булева переменная - наличие или отсутствие домашнего фактора
        """
        with open(league.get_matches_txt(), 'r') as matches:
            f = get_rid_of_slash_n(matches.readline())
        return f == 'field_factor=True'

    def config_teams(self):
        """
        Обновляет выпадающий список команд в окне настройки матчей
        """
        names = self.read_teams()
        for i in range(int(self.league.get_player_count() / 2)):
            for j in range(2):
                self.ui.teams[i][j].clear()
                self.ui.teams[i][j].addItems(names)

    def set_names(self):
        """
        Устанавливает нужные названия команд из списка в соответствии с сохранёнными данными в файле
        """
        matches = self.read_matches(self.league)
        for i, line in enumerate(matches):
            if i >= int(self.league.get_player_count() / 2):
                break
            index = [0] * 2
            for j in range(2):
                index[j] = self.ui.teams[i][j].findText(matches[i][j])
                self.ui.teams[i][j].setCurrentIndex(index[j])

    def set_field_factor(self):
        """
        Устанавливает наличие или отсутствие домашнего фактора в соответствии с сохранёнными данными в файле
        """
        if self.read_field_factor(self.league):
            self.ui.field_factor.widget.setCheckState(QtCore.Qt.Checked)

    def update_settings(self):
        """
        Обновляет параметры главного окна в соответствии с пользовательскими настройками
        """
        self.league = self.main_window.league
        self.ui.update_settings()
        self.config_teams()
        self.set_names()
        self.set_field_factor()
