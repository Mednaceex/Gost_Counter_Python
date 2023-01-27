from PyQt5 import QtCore

from modules.paths import matches_txt, players_txt
from modules.text_functions import split, get_rid_of_slash_n
from modules.classes import Dialog
from modules.custom_config import get_player_count
from windows.matches_ui import MatchesDialog


class Matches(Dialog):
    def __init__(self):
        """
        Конструктор класса окна настройки матчей
        """
        super(Matches, self).__init__()
        self.ui = MatchesDialog(self)
        self.config_teams()
        self.set_names()
        self.set_field_factor()
        self.ui.buttonBox.accepted.connect(self.save)
        self.setWindowTitle('Настройка матчей')

    def save(self):
        """
        Сохраняет данные о матчах в файл, вызывается при нажатии на кнопку "Сохранить"
        """
        self.save_matches(matches_txt)

    def save_matches(self, file):
        """
        Сохраняет данные о матчах в файл, создаёт сообщение об ошибке в случае

        :param file: путь к файлу
        """
        text = 'field_factor='
        text += 'True' if self.ui.field_factor.widget.isChecked() else 'False'
        for i in range(int(get_player_count() / 2)):
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
        teams = [''] * get_player_count()
        matches = self.read_matches()
        for i, line in enumerate(matches):
            if i >= int(get_player_count() / 2):
                break
            for j in range(2):
                teams[2 * i + j] = matches[i][j]
        return False if len(set(teams)) == len(teams) else True

    @staticmethod
    def read_teams():
        """
        Считывает названия команд из файла

        :return: список названий команд
        """
        with open(players_txt, 'r') as players:
            text = players.readlines()
        names = [split(line, ' - ')[0] for line in text]
        return names

    @staticmethod
    def read_matches():
        """
        Считывает матчи из файла

        :return: список матчей (каждый элемент списка - список из двух названий команд)
        """
        with open(matches_txt, 'r') as matches:
            text = matches.readlines()
        matches = [split(line, ' - ') for i, line in enumerate(text)]
        return matches[1::]

    @staticmethod
    def read_field_factor():
        """
        Считывает данные о факторе домашнего поля из файла

        :return: булева переменная - наличие или отсутствие домашнего фактора
        """
        with open(matches_txt, 'r') as matches:
            f = get_rid_of_slash_n(matches.readline())
        return f == 'field_factor=True'

    def config_teams(self):
        """
        Обновляет выпадающий список команд в окне настройки матчей
        """
        names = self.read_teams()
        for i in range(int(get_player_count() / 2)):
            for j in range(2):
                self.ui.teams[i][j].clear()
                self.ui.teams[i][j].addItems(names)

    def set_names(self):
        """
        Устанавливает нужные названия команд из списка в соответствии с сохранёнными данными в файле
        """
        matches = self.read_matches()
        for i, line in enumerate(matches):
            if i >= int(get_player_count() / 2):
                break
            index = [0] * 2
            for j in range(2):
                index[j] = self.ui.teams[i][j].findText(matches[i][j])
                self.ui.teams[i][j].setCurrentIndex(index[j])

    def set_field_factor(self):
        """
        Устанавливает наличие или отсутствие домашнего фактора в соответствии с сохранёнными данными в файле
        """
        if self.read_field_factor():
            self.ui.field_factor.widget.setCheckState(QtCore.Qt.Checked)

    def update_settings(self):
        """
        Обновляет параметры главного окна в соответствии с пользовательскими настройками
        """
        self.ui.update_settings()
        self.config_teams()
        self.set_names()
        self.set_field_factor()
