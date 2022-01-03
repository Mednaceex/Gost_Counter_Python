from PyQt5.QtWidgets import QApplication

from modules.paths import errors_txt, output_txt
from modules.classes import Dialog
from windows.results_ui import ResultsDialog


class Results(Dialog):
    def __init__(self):
        """
        Конструктор класса окна с итогами матчей
        """
        super(Results, self).__init__()
        self.ui = ResultsDialog(self)
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
        with open(output_txt, 'r') as results:
            results_text = results.readlines()
        with open(errors_txt, 'r') as errors:
            errors_text = errors.readlines()
        text = ''
        for line in results_text:
            text += line
        error_text = ''
        for line in errors_text:
            error_text += line
        self.ui.Text.setPlainText(text)
        self.ui.Errors.setPlainText(error_text)
