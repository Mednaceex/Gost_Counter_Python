from PyQt5 import QtCore

from modules.paths import custom_txt
from modules.text_functions import split, check_numbers
from modules.classes import Dialog
from modules.custom_config import player_count, match_count
from windows.settings_ui import SettingsDialog


class Settings(Dialog):
    def __init__(self):
        """
        Конструктор класса окна настроек
        """
        super(Settings, self).__init__()
        self.ui = SettingsDialog(self)
        self.set_data()
        self.ui.buttonBox.accepted.connect(self.save_data)
        self.setWindowTitle('Настройки')

    def save_data(self):
        """
        Сохраняет в файл введённые настройки, проверяет соответствие типов
        """
        players = check_numbers(self.ui.player_count.widget.text())
        matches = check_numbers(self.ui.match_count.widget.text())
        if players == '':
            players = player_count
        if matches == '':
            matches = match_count
        has_additional = self.ui.has_additional.widget.isChecked()
        # update = self.ui.auto_update.widget.isChecked()
        update = False
        text = 'player_count=' + str(players) + '\nmatch_count=' +\
               str(matches) + '\nhas_additional=' + str(has_additional) + '\nauto_update=' + str(update)
        with open(custom_txt, 'w') as custom:
            print(text, file=custom)

    def set_data(self):
        """
        Считывает из файла и выводит пользовательские настройки
        """
        with open(custom_txt, 'r') as custom:
            text = custom.readlines()
        d = {}
        for line in text:
            (param, value) = split(line, '=')
            d[param] = value
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
