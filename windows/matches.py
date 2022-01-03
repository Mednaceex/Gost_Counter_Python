from modules.paths import matches_txt, players_txt
from modules.text_functions import split
from modules.classes import Dialog
from modules.custom_config import player_count
from windows.matches_ui import MatchesDialog


class Matches(Dialog):
    def __init__(self):
        """
        Конструктор класса окна настройки матчей
        """
        super(Matches, self).__init__()
        self.ui = MatchesDialog(self)
        self.config_teams(self.read_teams())
        self.set_names()
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
        text = ''
        for i in range(int(player_count / 2)):
            name = [''] * 2
            for j in range(2):
                name[j] = self.ui.teams[i][j].currentText()
            if text != '':
                text += '\n'
            text += name[0] + ' - ' + name[1]
        with open(file, 'w') as matches:
            print(text, file=matches, end='')

    def check_repeats(self):
        """
        Проверяет наличие повторяющихся команд в настроенном расписании

        :return: True, если повторения есть, False иначе
        """
        teams = [''] * player_count
        matches = self.read_matches()
        for i, line in enumerate(matches):
            if i >= int(player_count / 2):
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
        return matches

    def config_teams(self, names):
        """
        Обновляет выпадающий список команд в окне настройки матчей

        :param names: список названий команд
        """
        for i in range(int(player_count / 2)):
            for j in range(2):
                self.ui.teams[i][j].clear()
                self.ui.teams[i][j].addItems(names)

    def set_names(self):
        """
        Устанавливает нужные названия команд из списка в соответствии с сохранёнными данными в файле
        """
        matches = self.read_matches()
        for i, line in enumerate(matches):
            if i >= int(player_count / 2):
                break
            index = [0] * 2
            for j in range(2):
                index[j] = self.ui.teams[i][j].findText(matches[i][j])
                self.ui.teams[i][j].setCurrentIndex(index[j])
