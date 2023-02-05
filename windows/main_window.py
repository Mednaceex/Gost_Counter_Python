from PyQt5 import QtCore, QtWidgets

from modules.const import end_symbol
from modules.text_functions import get_rid_of_slash_n, check_ascii, check_numbers, ending_ka
from modules.classes import BetText, Error, Result, League, Better
from modules.counter_functions import get_players, get_names, get_player_names, config_bets_list, check_for_no_errors,\
    count_all_bets, get_match, find_bet
from modules.custom_config import get_current_league

from windows.main_window_ui import MainWindow
from windows.matches import Matches
from windows.results import Results
from windows.teams import Teams
from windows.settings import Settings
from windows.leagues import Leagues


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Конструктор класса главного окна
        """
        super().__init__()
        self.set_league()
        self.ui = MainWindow(self)
        self.matches = Matches(self, self.league)
        self.teams = Teams(self, self.league)
        self.settings = Settings(self, self.league)
        self.results = Results(self, self.league)
        self.leagues = Leagues(self)
        self.bet_texts = []
        self.betters = []
        with open(self.league.get_players_txt(), 'r') as players:
            self.betters = get_players(players, self.league)
        self.set_names(get_names(self.betters), get_player_names(self.betters))
        self.open_saves()
        self.setWindowTitle('Счётчик гостов')

        self.ui.Matches_Button.clicked.connect(self.config_matches)
        self.ui.Teams_Button.clicked.connect(self.config_teams)
        self.ui.Settings_Button.clicked.connect(self.config_settings)
        self.ui.Leagues_Button.clicked.connect(self.config_leagues)
        self.ui.Save_Button.clicked.connect(self.save)
        self.ui.Count_Button.clicked.connect(self.count)
        self.ui.Reset_Button.clicked.connect(self.clear)
        if self.league.get_has_additional():
            self.ui.add_yes_box.clicked.connect(self.clear_additional_no)
            self.ui.add_no_box.clicked.connect(self.clear_additional_yes)

    def set_league(self):
        """
        Обновляет текущую лигу в соответствии с пользовательскими настройками
        :return:
        """
        self.league = League(get_current_league())

    def update_settings(self):
        """
        Обновляет параметры главного окна в соответствии с пользовательскими настройками
        """
        self.ui.update_league()
        self.ui.update_settings()
        self.bet_texts = []
        self.betters = []
        with open(self.league.get_players_txt(), 'r') as players:
            self.betters = get_players(players, self.league)
        self.set_names(get_names(self.betters), get_player_names(self.betters))
        self.open_saves()
        self.teams.update_settings()
        self.matches.update_settings()

    def update_league(self):
        """
        Обновляет лигу и все окна в соответствии с настройками и сохранёнными данными новой лиги
        """
        self.set_league()
        self.settings.set_data()
        self.update_settings()

    def save(self):
        """
        Сохраняет введённые значения в соответствующие файлы
        """
        self.set_league()
        self.save_texts(self.league.get_saved_txt())
        with open(self.league.get_scores_txt(), 'w') as score:
            print(self.save_scores(), file=score)
        self.save_checks(self.league.get_checks_txt())
        with open(self.league.get_additional_txt(), 'w') as add:
            print(self.save_additional(), file=add)
            print(self.save_additional_bets(), file=add)

    def count(self):
        """
        Сохраняет введённые данные, рассчитывает результаты матча и выводит на экран окно с ними
        """
        self.save()
        scores = self.get_scores()
        errors = self.get_goals_and_errors(scores)
        self.save_results()
        self.save_errors(errors, self.league.get_errors_txt(), self.matches.check_repeats())
        self.results.show_copied(False)
        self.results.print_results()
        self.results.show_on_top()

    def clear(self):
        """
        Очищает поля ввода текста, счета матчей и снимает все галочки
        """
        self.clear_scores()
        self.clear_checks()
        for bet_text in self.bet_texts:
            bet_text.text.setPlainText('')
        if self.league.get_has_additional():
            self.clear_additional()
            self.clear_additional_bets()

    def save_texts(self, file):
        """
        Сохраняет тексты гостов в файл

        :param file: путь к файлу
        """
        with open(file, 'w') as saved:
            for bet_text in self.bet_texts:
                text = check_ascii(bet_text.text.toPlainText().replace('\n', ' '))
                print(bet_text.name, file=saved)
                print(text, file=saved)
                print(end_symbol, file=saved)

    def save_checks(self, file):
        """
        Сохраняет данные о нажатых галочках в файл

        :param file: путь к файлу
        """
        with open(file, 'w') as checks:
            check_box = [self.ui.box_list[0].checks[0]]
            for i in range(self.league.get_player_count()):
                for j in range(self.league.get_match_count()):
                    check_box[0] = self.ui.box_list[i].checks[j]
                    if check_box[0].isChecked():
                        print(1, end='', file=checks)
                    else:
                        print(0, end='', file=checks)
                print('', file=checks)

    def save_additional_bets(self):
        """
        Возвращает дополнительные ставки в текстовом виде для сохранения в файл
        """
        if self.league.get_has_additional():
            text = ''
            for i in range(self.league.get_player_count()):
                if self.ui.box_list[i].add_yes.isChecked():
                    text += 'True\n'
                else:
                    if self.ui.box_list[i].add_no.isChecked():
                        text += 'False\n'
                    else:
                        text += 'None\n'
        else:
            text = 'None\n' * self.league.get_player_count()
        return text

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
            if check_for_no_errors(text, missing, self.league.get_match_count()):
                bets = config_bets_list(text, missing, self.league.get_match_count())
                if self.league.get_has_additional():
                    count_all_bets(bet_text.better, bets, scores,
                                    self.get_add_bet(bet_text.name), self.get_add_result())
                else:
                    count_all_bets(bet_text.better, bets, scores, self.betters)
            else:
                for better in self.betters:
                    if better.name == bet_text.name:
                        better.results = [Result(valid=False)] *\
                                         (self.league.get_match_count() + int(self.league.get_has_additional()))
                errors.append(Error(bet_text.name, len(find_bet(text))))
        return errors

    def save_results(self):
        """
        Составляет текст с результатами матча
        в соответствии с установленным расписанием и подсчитанным количеством голов каждой команды

        Сохраняет результаты матчей в файл вывода
        """
        output = self.league.get_output_txt()
        errors = self.league.get_errors_txt()
        text = Matches.read_matches(self.league)
        with open(self.league.get_output_txt(), 'w+'):
            pass
        for line in text:
            if line != '\n':
                get_match(line, output, errors, self.betters, Matches.read_field_factor(self.league),
                          self.league.get_match_count(), self.league.get_has_additional())

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
            else:
                print('Ошибок в гостах не найдено.', file=output)

    def config_matches(self):
        """
        Показывает окно настройки матчей
        """
        self.matches.update_settings()
        self.matches.show_on_top()
        self.matches.config_teams()
        self.matches.set_names()

    def config_teams(self):
        """
        Показывает окно настройки названий команд
        """
        self.teams.update_settings()
        self.teams.show_on_top()
        self.teams.set_names()

    def config_settings(self):
        """
        Показывает окно настроек
        """
        self.settings.show_on_top()
        self.settings.set_data()

    def config_leagues(self):
        """
        Показывает окно настройки и выбора лиги
        """
        self.leagues.show_on_top()
        self.leagues.set_data()

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
            better = Better(self.league, elem)
            for b in self.betters:
                if b.name == elem:
                    better = b
            self.bet_texts.append(BetText(better, self.ui.box_list[i].text, i))

    def get_missing(self, name):
        """
        Определяет, какие матчи в госте данного игрока пропущены

        :param name: название команды
        :return: список из значений True (матч пропущен) или False (матч присутствует)
        """
        array = [True] * self.league.get_match_count()
        for bet_text in self.bet_texts:
            if bet_text.name == name:
                for i in range(self.league.get_match_count()):
                    array[i] = self.ui.box_list[bet_text.number].checks[i].isChecked()
        return array

    def open_saves(self):
        """
        Открывает сохранённые данные из файлов
        """
        with open(self.league.get_saved_txt(), 'r') as saved:
            saves = saved.readlines()
        with open(self.league.get_scores_txt(), 'r') as score:
            scores = score.readlines()
        with open(self.league.get_additional_txt(), 'r') as additionals:
            add = additionals.readlines()
        saves_text = [get_rid_of_slash_n(line) for i, line in enumerate(saves)]
        scores_text = [get_rid_of_slash_n(line) for i, line in enumerate(scores)]
        additional = get_rid_of_slash_n(add[0])
        self.set_scores(scores_text)
        self.config_bet_texts(saves_text)
        self.open_checks()
        if self.league.get_has_additional():
            self.open_additional(additional)
            text = [get_rid_of_slash_n(add[i]) for i in range(1, len(add), 1)]
            self.open_additional_bets(text)

    def config_bet_texts(self, saves_text):
        """
        Помещает сохранённые тексты гостов в соответствующие окна

        :param saves_text: текст сохранённых гостов из файла
        """
        i = 0
        while i < len(saves_text):
            for bet_text in self.bet_texts:
                if bet_text.better.name == saves_text[i]:
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
        with open(self.league.get_checks_txt(), 'r') as checks:
            text = checks.readlines()
        for i, line in enumerate(text):
            if i >= self.league.get_player_count():
                break
            for j, char in enumerate(line):
                if j >= self.league.get_match_count():
                    break
                if text[i][j] == '1':
                    self.ui.box_list[i].checks[j].setCheckState(QtCore.Qt.Checked)

    def open_additional(self, text):
        """
        Открывает сохранённые данные об исходе дополнительной ставки
        :param text: строка из файла с данными о дополнительной ставке
        """
        if text == "True":
            self.ui.add_yes_box.setCheckState(QtCore.Qt.Checked)
        if text == "False":
            self.ui.add_no_box.setCheckState(QtCore.Qt.Checked)

    def open_additional_bets(self, text: list):
        """
        Открывает сохранённые данные о дополнительных ставках игроков
        :param text: список строк из файла с данными о дополнительной ставке
        """
        for i in range(min(len(text), self.league.get_player_count())):
            if text[i] == "True":
                self.ui.box_list[i].add_yes.setCheckState(QtCore.Qt.Checked)
            if text[i] == "False":
                self.ui.box_list[i].add_no.setCheckState(QtCore.Qt.Checked)

    def get_scores(self):
        """
        Считывает счета матчей из полей для ввода

        :return: список счетов матчей
        Каждый элемент возвращаемого списка - список из 2 чисел - ставок на 1 и 2 команды
        """
        scores = []
        for i in range(self.league.get_match_count()):
            scores.append([check_numbers(self.ui.scores[i][0].text()), check_numbers(self.ui.scores[i][1].text())])
            if scores[i][0] == '' or scores[i][1] == '':
                scores[i] = 'None'
        return scores

    def get_add_bet(self, name: str):
        """
        Определяет дополнительную ставку игрока

        :param name: название команды
        :return: результат ставки или 'None' если он не указан
        """
        if self.league.get_has_additional():
            i = 0
            for bet_text in self.bet_texts:
                if bet_text.name == name:
                    i = bet_text.number
            if self.ui.box_list[i].add_yes.isChecked():
                return 'True'
            else:
                if self.ui.box_list[i].add_no.isChecked():
                    return 'False'
                else:
                    return 'None'
        else:
            return 'None'

    def get_add_result(self):
        """
        Определяет результат дополнительной ставки

        :return: результат ставки или 'None' если он не указан
        """
        if self.league.get_has_additional():
            if self.ui.add_yes_box.isChecked():
                return 'True'
            else:
                if self.ui.add_no_box.isChecked():
                    return 'False'
                else:
                    return 'None'
        else:
            return 'None'

    def save_scores(self):
        """
        Возвращает счета матчей в текстовом виде для сохранения в файл
        """
        text = ''
        for i in range(self.league.get_match_count()):
            score = [''] * 2
            for j in range(2):
                score[j] = check_numbers(self.ui.scores[i][j].text())
            text += score[0] + '\n' + score[1] + '\n'
        return text

    def save_additional(self):
        """
        Возвращает результат дополнительной ставки в текстовом виде для сохранения в файл
        """
        if self.league.get_has_additional():
            if self.ui.add_yes_box.isChecked():
                text = 'True'
            else:
                if self.ui.add_no_box.isChecked():
                    text = 'False'
                else:
                    text = 'None'
        else:
            text = 'None'
        return text

    def clear_scores(self):
        """
        Очищает поля для ввода счетов матчей
        """
        empty = ''
        for i in range(self.league.get_match_count()):
            for j in range(2):
                self.ui.scores[i][j].setText(empty)

    def clear_checks(self):
        """
        Снимает все галочки
        """
        for i in range(self.league.get_player_count()):
            for j in range(self.league.get_match_count()):
                self.ui.box_list[i].checks[j].setCheckState(QtCore.Qt.Unchecked)

    def clear_additional(self):
        """
        Снимает галочки в окошке дополнительной ставки
        """
        self.clear_additional_yes()
        self.clear_additional_no()

    def clear_additional_yes(self):
        """
        Снимает галочку "Да" в окошке дополнительной ставки
        """
        self.ui.add_yes_box.setCheckState(QtCore.Qt.Unchecked)

    def clear_additional_no(self):
        """
        Снимает галочку "Нет" в окошке дополнительной ставки
        """
        self.ui.add_no_box.setCheckState(QtCore.Qt.Unchecked)

    def clear_additional_bets(self):
        """
        Снимает галочки дополнительных ставок в окошках с гостами
        """
        for i in range(self.league.get_player_count()):
            self.ui.box_list[i].add_yes.setCheckState(QtCore.Qt.Unchecked)
            self.ui.box_list[i].add_no.setCheckState(QtCore.Qt.Unchecked)

    def set_scores(self, text: list):
        """
        Выводит на экран сохранённые счета матчей

        :param text: текст сохранённых счетов
        (список строк, по 1 числу в каждой строке, на 1 матч должно выделяться 2 строки)
        """
        score_array = text[0:2 * self.league.get_match_count():1]
        for i in range(int(len(score_array) / 2)):
            for j in range(2):
                self.ui.scores[i][j].setText(get_rid_of_slash_n(score_array[2 * i + j]))

    def update_betters_league(self, old_league_name: str, new_league_name: str):
        for better in self.betters:
            if better.league.name == old_league_name:
                better.league = League(new_league_name)
        for text in self.bet_texts:
            if text.better.league.name == old_league_name:
                text.better.league = League(new_league_name)
