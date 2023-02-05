from modules.text_functions import split, sort_lines_alphabetical, check_ascii_russian
from modules.classes import Dialog, League
from windows.teams_ui import TeamsDialog


class Teams(Dialog):
    def __init__(self, main_window, league: League):
        """
        Конструктор класса окна настройки названий команд

        :param league: лига, в которой играют команды
        """
        super(Teams, self).__init__()
        self.league = league
        self.ui = TeamsDialog(self)
        self.set_names()
        self.main_window = main_window
        self.ui.buttonBox.accepted.connect(self.save)
        self.setWindowTitle('Настройка команд')

    def save(self):
        """
        Сохраняет названия команд и имена игроков в файл
        """
        text = self.save_players()
        with open(self.league.get_players_txt(), 'w') as players:
            print(sort_lines_alphabetical(text), file=players, end='')
        self.main_window.update_settings()

    def save_players(self):
        """
        Возвращает строку с названиями команд в формате Команда - Имя, разделённые символом "\n"
        """
        text = ''
        for i in range(self.league.get_player_count()):
            name = [''] * 2
            name[0] += check_ascii_russian(self.ui.teams[i].text())
            name[1] += check_ascii_russian(self.ui.names[i].text())
            if text != '':
                text += '\n'
            text += name[0] + ' - ' + name[1]
        return text

    def set_names(self):
        """
        Считывает из файла и выводит названия команд и имена игроков
        """
        with open(self.league.get_players_txt(), 'r') as players:
            text = players.readlines()
        for i, line in enumerate(text):
            if i >= self.league.get_player_count():
                break
            (team, name) = split(line, ' - ')
            self.ui.teams[i].setText(team)
            self.ui.names[i].setText(name)

    def update_settings(self):
        """
        Обновляет параметры главного окна в соответствии с пользовательскими настройками
        """
        self.league = self.main_window.league
        self.ui.update_settings()
        self.set_names()
