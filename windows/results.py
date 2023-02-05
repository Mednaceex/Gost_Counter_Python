from PyQt5.QtWidgets import QApplication

from modules.classes import Dialog, League
from windows.results_ui import ResultsDialog


class Results(Dialog):
    def __init__(self, main_window, league: League):
        """
        Конструктор класса окна с итогами матчей

        :param league: лига, в которой проходят матчи
        """
        super().__init__()
        self.main_window = main_window
        self.ui = ResultsDialog(self)
        self.league = league
        self.print_results()
        self.setWindowTitle('Результаты матчей')
        self.show_copied(False)

        self.ui.Copy_Button.clicked.connect(self.copy)
        self.ui.Exit_Button.clicked.connect(self.close)

    def copy(self):
        """
        Копирует текст результатов в буфер обмена, показывает надпись "Скопировано"
        """
        text = self.ui.Text.toPlainText()
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)
        self.show_copied(True)

    def show_copied(self, boolean):
        """
        Отображает надпись "Скопировано" или скрывает её

        :param boolean: переменная логического типа, определяет, нужно ли показывать надпись "Скопировано"
        """
        if boolean:
            self.ui.Copied_Label.setText('Скопировано!')
        else:
            self.ui.Copied_Label.setText('')

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
        if error_text:
            while error_text[-1] == '\n':
                error_text = error_text[:-1]
        if text:
            while text[-1] == '\n':
                text = text[:-1]
        self.ui.Text.setPlainText(text)
        self.ui.Errors.setPlainText(error_text)
