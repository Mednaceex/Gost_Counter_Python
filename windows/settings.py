from PyQt5 import QtCore

from modules.paths import custom_txt
from modules.text_functions import split
from modules.classes import Dialog
from windows.settings_ui import SettingsDialog


class Settings(Dialog):
    def __init__(self):
        """
        Конструктор класса окна с итогами матчей
        """
        super(Settings, self).__init__()
        self.ui = SettingsDialog(self)
        self.set_data()
        self.ui.buttonBox.accepted.connect(self.save_data)
        self.setWindowTitle('Настройки')

    def save_data(self):
        players = self.ui.player_count.widget.text()
        matches = self.ui.match_count.widget.text()
        update = self.ui.auto_update.widget.isChecked()
        text = 'player_count=' + players + '\nmatch_count=' + matches + '\nauto_update=' + str(update)
        with open(custom_txt, 'w') as custom:
            print(text, file=custom)

    def set_data(self):
        """
        Считывает из файла и выводит названия команд и имена игроков
        """
        with open(custom_txt, 'r') as custom:
            text = custom.readlines()
        d = {}
        for line in text:
            (param, value) = split(line, '=')
            d[param] = value
        self.ui.player_count.widget.setText(d['player_count'])
        self.ui.match_count.widget.setText(d['match_count'])
        if d['auto_update'] == 'True':
            self.ui.auto_update.widget.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.auto_update.widget.setCheckState(QtCore.Qt.Unchecked)
