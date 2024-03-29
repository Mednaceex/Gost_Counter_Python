from PyQt5 import QtCore

from modules.text_functions import check_numbers
from modules.classes import Dialog, League
from modules.custom_config import get_max_player_count, get_max_match_count
from windows.settings_ui import SettingsUI


class Settings(Dialog):
    def __init__(self, main_window, league: League):
        """
        Конструктор класса окна настроек

        :param league: лига, к которой применяются настройки
        """
        super(Settings, self).__init__()
        self.ui = SettingsUI(self)
        self.league = league
        self.main_window = main_window
        self.set_data()
        self.ui.Choose_Button.clicked.connect(self.save_data)
        self.ui.Cancel_Button.clicked.connect(self.close)
        self.setWindowTitle('Настройки')

    def save_data(self):
        """
        Сохраняет в файл введённые настройки, проверяет соответствие типов, закрывает окно, обновляет главное окно
        """
        self.league = self.main_window.league
        players = check_numbers(self.ui.player_count.widget.text())
        matches = check_numbers(self.ui.match_count.widget.text())
        if players == '':
            players = self.league.get_player_count()
        if matches == '':
            matches = self.league.get_match_count()
        if int(players) > get_max_player_count():
            players = str(get_max_player_count())
        if int(matches) > get_max_match_count():
            matches = str(get_max_match_count())
        has_additional = self.ui.has_additional.widget.isChecked()
        # update = self.ui.auto_update.widget.isChecked()
        update = False
        text = 'player_count=' + str(players) + '\nmatch_count=' +\
               str(matches) + '\nhas_additional=' + str(has_additional) + '\nauto_update=' + str(update)
        with open(self.league.get_custom_txt(), 'w') as custom:
            print(text, file=custom)
        self.main_window.update_settings()
        self.close()

    def set_data(self):
        """
        Считывает из файла и выводит пользовательские настройки
        """
        self.league = self.main_window.league
        d = self.league.get_custom_data()
        self.ui.player_count.widget.setText(d['player_count'])
        self.ui.match_count.widget.setText(d['match_count'])
        if d['has_additional'] == 'True':
            self.ui.has_additional.widget.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.has_additional.widget.setCheckState(QtCore.Qt.Unchecked)
        # if d['auto_update'] == 'True':
            # self.ui.auto_update.widget.setCheckState(QtCore.Qt.Checked)
            # else:
            # self.ui.auto_update.widget.setCheckState(QtCore.Qt.Unchecked)
