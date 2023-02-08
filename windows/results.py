from PyQt5.QtWidgets import QApplication

from modules.text_functions import remove_final_empty_lines
from modules.classes import Dialog, League
from windows.results_ui import ResultsUI


class Results(Dialog):
    def __init__(self, main_window, league: League):
        """
        Конструктор класса окна с итогами матчей

        :param league: лига, в которой проходят матчи
        """
        super().__init__()
        self.main_window = main_window
        self.ui = ResultsUI(self)
        self.league = league
        self.print_results()
        self.setWindowTitle('Результаты матчей')
        self.show_copied(False)

        self.ui.Choose_Button.clicked.connect(self.copy)
        self.ui.Cancel_Button.clicked.connect(self.close)

    def copy(self):
        """
        Копирует текст результатов в буфер обмена, показывает надпись "Скопировано"
        """
        text = self.ui.Text.toPlainText()
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)
        self.show_copied(True)

    def show_copied(self, showed: bool):
        """
        Отображает надпись "Скопировано" или скрывает её

        :param showed: определяет, нужно ли показывать надпись "Скопировано"
        """
        self.ui.Copied_Label.setText('Скопировано!' if showed else '')

    def print_results(self):
        """
        Считывает из файлов и выводит на экран результаты матчей и данные об ошибках в гостах
        """
        self.league = self.main_window.league
        with open(self.league.get_output_txt(), 'r') as results:
            results_text = results.readlines()
        with open(self.league.get_errors_txt(), 'r') as errors:
            errors_text = errors.readlines()
        text = ''
        for line in results_text:
            text += line
        error_text = ''
        for line in errors_text:
            error_text += line
        error_text = remove_final_empty_lines(error_text)
        text = remove_final_empty_lines(text)
        self.ui.Text.setPlainText(text)
        self.ui.Errors.setPlainText(error_text)
