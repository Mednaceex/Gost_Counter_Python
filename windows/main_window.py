from PyQt5 import QtCore, QtWidgets

from modules.const import end_symbol
from modules.paths import players_txt, saved_txt, scores_txt, checks_txt, errors_txt, output_txt, matches_txt
from modules.text_functions import get_rid_of_slash_n, check_ascii, check_numbers, ending_ka
from modules.classes import BetText, Error
from modules.counter_functions import get_players, get_names, get_player_names, config_bets_list, count_goals, get_match
from modules.custom_config import player_count, match_count

from windows.main_window_ui import MainWindow
from windows.matches import Matches
from windows.results import Results
from windows.teams import Teams
from windows.settings import Settings


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Конструктор класса главного окна
        """
        super(Window, self).__init__()
        self.ui = MainWindow(self)
        self.matches = Matches()
        self.teams = Teams()
        self.settings = Settings()
        self.results = Results()
        self.bet_texts = []
        with open(players_txt, 'r') as players:
            self.betters = get_players(players)
        self.set_names(get_names(self.betters), get_player_names(self.betters))
        self.open_saves()
        self.setWindowTitle('Счётчик гостов')

        self.ui.Matches_Button.clicked.connect(self.config_matches)
        self.ui.Teams_Button.clicked.connect(self.config_teams)
        self.ui.Settings_Button.clicked.connect(self.config_settings)
        self.ui.Save_Button.clicked.connect(self.save)
        self.ui.Count_Button.clicked.connect(self.count)
        self.ui.Reset_Button.clicked.connect(self.clear)

    def save(self):
        """
        Сохраняет введённые значения в соответствующие файлы
        """
        with open(saved_txt, 'w') as saved:
            for bet_text in self.bet_texts:
                text = check_ascii(bet_text.text.toPlainText())
                print(bet_text.name, file=saved)
                print(text, file=saved)
                print(end_symbol, file=saved)
        with open(scores_txt, 'w') as score:
            print(self.save_scores(), file=score)
        self.save_checks(checks_txt)

    def count(self):
        """
        Сохраняет введённые данные, рассчитывает результаты матча и выводит на экран окно с ними
        """
        self.save()
        scores = self.get_scores()
        errors = self.get_goals_and_errors(scores)
        self.save_results()
        self.save_errors(errors, errors_txt, self.matches.check_repeats())
        self.results.show_copied(False)
        self.results.print_results()
        self.results.show()

    def clear(self):
        """
        Очищает поля ввода текста, счета матчей и снимает все галочки
        """
        self.clear_scores()
        self.clear_checks()
        for bet_text in self.bet_texts:
            bet_text.text.setPlainText('')

    def save_checks(self, file):
        """
        Сохраняет данные о нажатых галочках в файл

        :param file: путь к файлу
        """
        with open(file, 'w') as checks:
            check_box = [self.ui.box_list[0].checks[0]]
            for i in range(player_count):
                for j in range(match_count):
                    check_box[0] = self.ui.box_list[i].checks[j]
                    if check_box[0].isChecked():
                        print(1, end='', file=checks)
                    else:
                        print(0, end='', file=checks)
                print('', file=checks)

    def get_goals_and_errors(self, scores):
        """
        Анализирует введённые госты на наличие ошибок
        Считает количество забитых командами голов для корректных гостов,
        возвращает сведения об ошибках в остальных гостах

        :param scores: список счетов реальных матчей
        :return: список ошибок в гостах (объектов класса Error)
        """
        errors = []
        for bet_text in self.bet_texts:
            text = check_ascii(bet_text.text.toPlainText())
            missing = self.get_missing(bet_text.name)
            bets = config_bets_list(text, missing)
            if type(bets) is int:
                for better in self.betters:
                    if better.name == bet_text.name:
                        better.goals = 0
                errors.append(Error(bet_text.name, bets))
            else:
                count_goals(bet_text.name, bets, scores, self.betters)
        return errors

    def save_results(self):
        """
        Составляет текст с результатами матча
        в соответствии с установленным расписанием и подсчитанным количеством голов каждой команды

        Сохраняет результаты матчей в файл вывода
        """
        with open(output_txt, 'w+') as output:
            with open(matches_txt, 'r') as matches:
                text = matches.readlines()
            for line in text:
                if line != '\n':
                    get_match(line, output, self.betters)

    @staticmethod
    def save_errors(errors_list: list[Error], output_file, repeats=False):
        """
        Генерирует сообщения об ошибках в гостах на основе полученного списка ошибок и сохраняет их в файл

        :param errors_list: список ошибок в гостах (объектов класса Error)
        :param output_file: путь к файлу вывода сообщений об ошибках
        :param repeats: определяет, есть ли повторяющиеся команды в расписании матчей
        """
        with open(output_file, 'w') as output:
            if repeats:
                print('Ошибка в расписании: есть повторяющиеся команды\n', file=output)
            if errors_list:
                for error in errors_list:
                    count = f'({error.number} став' + ending_ka(error.number) + ')'
                    print('Ошибка в госте:', error.name, count, file=output)

    def config_matches(self):
        """
        Показывает окно настройки матчей
        """
        self.matches.show()
        self.matches.config_teams(self.matches.read_teams())
        self.matches.set_names()

    def config_teams(self):
        """
        Показывает окно настройки названий команд
        """
        self.teams.show()
        self.teams.set_names()

    def config_settings(self):
        """
        Показывает окно настроек
        """
        self.settings.show()
        self.settings.set_data()

    def set_names(self, name_array, player_name_array):
        """
        Устанавливает названия команд на экране, определяет список объектов класса BetText с текстами гостов

        :param name_array: список названий команд
        :param player_name_array: список имён игроков
        """
        for i, elem in enumerate(name_array):
            if i >= len(self.ui.box_list):
                break
            self.ui.box_list[i].name.setText(player_name_array[i])
            self.bet_texts.append(BetText(elem, self.ui.box_list[i].text, i))

    def get_missing(self, name):
        """
        Определяет, какие матчи в госте данного игрока пропущены

        :param name: название команды
        :return: список из значений True (матч пропущен) или False (матч присутствует)
        """
        array = [True] * match_count
        for bet_text in self.bet_texts:
            if bet_text.name == name:
                for i in range(match_count):
                    array[i] = self.ui.box_list[bet_text.number].checks[i].isChecked()
        return array

    def open_saves(self):
        """
        Открывает сохранённые данные из файлов
        """
        with open(saved_txt, 'r') as saved:
            saves = saved.readlines()
        with open(scores_txt, 'r') as score:
            scores = score.readlines()
        saves_text = [get_rid_of_slash_n(saves[i]) for i, line in enumerate(saves)]
        scores_text = [get_rid_of_slash_n(scores[i]) for i, line in enumerate(scores)]
        self.set_scores(scores_text)
        self.config_bet_texts(saves_text)
        self.open_checks()

    def config_bet_texts(self, saves_text):
        """
        Помещает сохранённые тексты гостов в соответствующие окна

        :param saves_text: текст сохранённых гостов из файла
        """
        i = 0
        while i < len(saves_text):
            for bet_text in self.bet_texts:
                if bet_text.name == saves_text[i]:
                    i += 1
                    text = ''
                    while saves_text[i] != end_symbol:
                        if text != '':
                            text += '\n'
                        text += saves_text[i]
                        i += 1
                    self.ui.box_list[bet_text.number].text.setPlainText(text)
            i += 1

    def open_checks(self):
        """
        Открывает сохранённые данные о нажатых галочках из файла
        """
        with open(checks_txt, 'r') as checks:
            text = checks.readlines()
        for i, line in enumerate(text):
            if i >= player_count:
                break
            for j, char in enumerate(line):
                if j >= player_count:
                    break
                if text[i][j] == '1':
                    self.ui.box_list[i].checks[j].setCheckState(QtCore.Qt.Checked)

    def get_scores(self):
        """
        Считывает счета матчей из полей для ввода

        :return: список счетов матчей
        Каждый элемент возвращаемого списка - список из 2 чисел - ставок на 1 и 2 команды
        """
        scores = []
        for i in range(match_count):
            scores.append([check_numbers(self.ui.scores[i][0].text()), check_numbers(self.ui.scores[i][1].text())])
            if scores[i][0] == '' or scores[i][1] == '':
                scores[i] = 'None'
        return scores

    def save_scores(self):
        """
        Возвращает счета матчей в текстовом виде для сохранения в файл
        """
        text = ''
        for i in range(match_count):
            score = [''] * 2
            for j in range(2):
                score[j] = check_numbers(self.ui.scores[i][j].text())
            text += score[0] + '\n' + score[1] + '\n'
        return text

    def clear_scores(self):
        """
        Очищает поля для ввода счетов матчей
        """
        empty = ''
        for i in range(match_count):
            for j in range(2):
                self.ui.scores[i][j].setText(empty)

    def clear_checks(self):
        """
        Снимает все галочки
        """
        for i in range(player_count):
            for j in range(match_count):
                self.ui.box_list[i].checks[j].setCheckState(QtCore.Qt.Unchecked)

    def set_scores(self, text: list):
        """
        Выводит на экран сохранённые счета матчей

        :param text: текст сохранённых счетов
        (список строк, по 1 числу в каждой строке, на 1 матч должно выделяться 2 строки)
        """
        score_array = text[0:2 * match_count:1]
        for i in range(int(len(score_array) / 2)):
            for j in range(2):
                self.ui.scores[i][j].setText(get_rid_of_slash_n(score_array[2 * i + j]))
