from PyQt5 import QtCore

from modules.text_functions import split, get_rid_of_slash_n, check_ascii_russian
from modules.classes import Dialog, League
from modules.custom_config import get_current_league, get_leagues, set_current_league
from windows.leagues_ui import LeaguesDialog
from windows.confirm_window import DeleteConfirmWindow, RenameConfirmWindow, AddLeague


class Leagues(Dialog):
    def __init__(self, main_window):
        """
        Конструктор класса окна настройки и выбора лиги
        """
        super(Leagues, self).__init__()
        self.ui = LeaguesDialog(self)
        self.add_league_window = AddLeague(self)
        self.main_window = main_window
        self.delete_confirm_window = DeleteConfirmWindow(self)
        self.rename_confirm_window = RenameConfirmWindow(self)
        self.setWindowTitle('Выбор лиги')
        self.connect_buttons()
        self.current_league = get_current_league()
        self.league_list = get_leagues()
        if self.current_league not in self.league_list:
            self.current_league = 'default'

    def connect_buttons(self):
        self.ui.Cancel_Button.clicked.connect(self.exit)
        self.ui.Add_Button.clicked.connect(self.add_league)
        for i, league in enumerate(self.ui.league_list):
            self.ui.box_list[i].Choose_Button.clicked.connect(self.generate_choose_function(league))
            self.ui.box_list[i].Rename_Button.clicked.connect(self.generate_rename_function(league))
            self.ui.box_list[i].Delete_Button.clicked.connect(self.generate_delete_function(league))

    def exit(self):
        self.close()
        self.rename_confirm_window.close()
        self.delete_confirm_window.close()

    def add_league(self):
        self.add_league_window.show_on_top()

    def set_data(self):
        self.ui.remove_boxes()
        self.ui.set_boxes(get_leagues())
        self.ui.set_current_label(get_current_league())
        self.connect_buttons()
        self.main_window.ui.set_league_name(get_current_league())

    def generate_choose_function(self, league_name: str):
        def func():
            self.ui.set_current_label(league_name)
            self.current_league = league_name
            set_current_league(league_name)
            self.ui.error_label.hide()
            self.main_window.set_league()
            self.main_window.update_settings()
        return func

    def generate_rename_function(self, league_name: str):
        def func():
            self.delete_confirm_window.close()
            self.rename_confirm_window.open_(league_name)
            self.ui.error_label.hide()
        return func

    def generate_delete_function(self, league_name: str):
        def func():
            if get_current_league() != league_name:
                self.rename_confirm_window.close()
                self.delete_confirm_window.open_(league_name)
                self.ui.error_label.hide()
            else:
                self.ui.error_label.show()
        return func

