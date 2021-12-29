import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore

from windows.main_window import Ui_MainWindow
from windows.matches import Ui_Dialog
from windows.teams import Ui_Dialog as Ui_Dialog_2
from windows.results import Ui_Dialog as Ui_Dialog_3
from windows.settings import Ui_Dialog as Ui_Dialog_4

none = ('xx', 'хх', 'ХХ', 'XX', '__', '--', '_', '//', '/', '', 'None')
match_count = 10
player_count = 20
long_seps = (' -:- ', '—:—', ' -:-', '-:- ', '-:-')
seps = ('-', '—')
numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
end_symbol = '//'

saved_txt = Path('data', 'saved.txt')
errors_txt = Path('data', 'errors.txt')
checks_txt = Path('data', 'checks.txt')
matches_txt = Path('data', 'matches.txt')
output_txt = Path('data', 'output.txt')
players_txt = Path('data', 'players.txt')


class Better:
    def __init__(self, name: str, goals=0):
        """
        Конструктор класса игроков

        :param name: название команды игрока
        :param goals: количество голов, забитых игроком
        """
        self.name = name
        self.player_name = self.get_name()
        self.goals = goals

    def set_goals(self, value):
        """
        Изменяет количество голов игрока на заданное параметром value
        """
        self.goals = value

    def get_name(self):
        """
        Считывает имя игрока из файла

        :return: имя игрока (строка)
        """
        name = ''
        with open(players_txt, 'r') as players:
            text = players.readlines()
            for line in text:
                player = split(line, ' - ')
                if player[0] == self.name:
                    name = player[1]
        return name


def check_ascii(string: str):
    """
    Исключает из строки все символы, не входящие в первые 127 символов таблицы ASCII или не являющиеся символом '—'

    :param string: строка
    :return: новая строка
    """
    new_string = ''
    for char in string:
        if 0 < ord(char) < 128 and ord(char) != ord('—'):
            new_string += char
    return new_string


def sort_lines_alphabetical(string: str):
    """
    Сортирует строки (разделённые символом "\n") в алфавитном порядке, возвращает полученную строку

    :return: отсортированная строка
    """
    array = split(string, '\n')
    array.sort()
    sorted_string = ''
    for line in array:
        if sorted_string != '':
            sorted_string += '\n'
        sorted_string += line
    return sorted_string


def count_bet(bet1: int, bet2: int, score1: int, score2: int):
    """
    Определяет и возвращает количество голов, забитых на конкретной ставке

    :param bet1: инд. тотал 1 команды в ставке
    :param bet2: инд. тотал 2 команды в ставке
    :param score1: реальный инд. тотал 1 команды
    :param score2: реальный инд. тотал 2 команды
    """
    if (bet1 == score1) and (bet2 == score2):
        return 2
    elif (bet1 < bet2) and (score1 < score2):
        return 1
    elif (bet1 > bet2) and (score1 > score2):
        return 1
    elif (bet1 == bet2) and (score1 == score2):
        return 1
    else:
        return 0


def split(string: str, sep=None):
    """
    Разделяет строку на список по данной разделительной строке, удаляет символы перехода на новую строку

    :param string: строка, которую необходимо разделить
    :param sep: разделительная строка
    :return: список строк
    """
    if sep is None:
        array = [string]
    else:
        array = string.split(sep)
    for j, elem in enumerate(array):
        array[j] = get_rid_of_slash_n(elem)
    return array


def get_rid_of_slash_n(string: str):
    """
    Удаляет символы "\n" из строки

    :param string: строка
    :return: обработанная строка
    """
    return string.replace('\n', '')


def ending_ka(number):
    """
    Определяет окончания слов, заканчивающихся на "ка", употреблённых с числом

    :param number: употреблённое число
    :return: строка, на которую заменяется "ка" в конце слова
    """
    if 5 <= number <= 20:
        return 'ок)'
    elif number % 10 == 1:
        return 'ка)'
    elif 2 <= number % 10 <= 4:
        return 'ки)'
    else:
        return 'ок)'


def get_players(file):
    """
    Считывает названия команд и имена тренеров из файла, создаёт список объектов класса Better с этими данными

    :param file: путь к файлу
    :return: список объектов класса Better
    """
    array = []
    text = file.readlines()
    for line in text:
        a = split(line, ' - ')
        b = Better(a[0])
        array.append(b)
    return array


def get_names(betters_array):
    """
    Возвращает список названий команд

    :param betters_array: список объектов класса Better
    :return: список названий команд из полученного списка
    """
    return [better.name for better in betters_array]


def get_player_names(betters_array):
    """
    Возвращает список названий команд с именами игроков

    :param betters_array: список объектов класса Better
    :return: список названий команд с именами игроков из полученного списка
    Формат строки в списке: Команда (Имя)
    """
    return [better.name + ' (' + better.player_name + ')' for better in betters_array]


def count_goals(name, bets_list, scores_list, betters_list):
    """
    Рассчитывает количество забитых игроком голов и устанавливает это значение у соответствующего объекта Better

    :param name: название команды
    :param bets_list: список ставок игрока
    :param scores_list: список счетов реальных матчей
    :param betters_list: список игроков (объектов класса Better)
    """
    goals = 0
    bets = ['None'] * match_count
    for i, bet in enumerate(bets_list):
        if bet in none:
            bets[i] = 'None'
        else:
            bets[i] = bet
    for i, bet in enumerate(bets):
        if bet != 'None' and scores_list[i] != 'None':
            goals += count_bet(int(bet[0]), int(bet[1]), int(scores_list[i][0]), int(scores_list[i][1]))
    for i in betters_list:
        if i.name == name:
            i.set_goals(goals)


def get_match(line, output_file, betters_list):
    """
    Считывает матч из строки расписания и выводит его счёт в файл вывода

    :param line: строка с матчем из расписания
    :param output_file: путь к файлу вывода
    :param betters_list: список игроков (объектов класса Better)
    """
    array = split(line, ' - ')
    g = [0] * 2
    name = [''] * 2
    for i in betters_list:
        for k in range(2):
            if i.name == array[k]:
                g[k] = i.goals
                name[k] = i.name
    for k in range(2):
        if name[k] == '':
            print_name_error(array[k], output_file)
    else:
        print(name[0], f'{g[0]}-{g[1]}', name[1], file=output_file)


def bets_from_text(text: str):
    """
    Ищет ставки игрока, разделённые символом ":", в тексте госта и возвращает список с ними

    :return: Список найденных ставок, каждый элемент которого - список из 2 чисел - ставок на 1 и 2 команды
    """
    array = []
    for i, character in enumerate(text):
        if character == ':' and 0 < i < len(text)-1:
            if text[i-1] in numbers and text[i+1] in numbers:
                (bet1, bet2) = ('', '')
                (left, right) = (1, 1)
                while i - left > 1 and text[i - left - 1] in numbers:
                    left += 1
                while i + right < len(text) - 2 and text[i + right + 1] in numbers:
                    right += 1
                for j in range(left):
                    bet1 += text[i - left + j]
                for j in range(right):
                    bet2 += text[i + j + 1]
                array.append([int(bet1), int(bet2)])
    return array


def find_bet(text: str):
    """
    Ищет ставки игрока, разделённые одним из допустимых символов или строк, в тексте госта и возвращает список с ними

    :return: Список найденных ставок, каждый элемент которого - список из 2 чисел - ставок на 1 и 2 команды
    """
    for string in long_seps:
        text = text.replace(string, ':')
    for string in seps:
        text = text.replace(string, ':')
    return bets_from_text(text)


def config_bets_array(text: str, missing: list, count=match_count):
    """
    Считывает ставки из текста госта, присланного игроком

    :param text: текст госта
    :param missing: список из count элементов - True (ставка отсутствует) или False (ставка есть)
    :param count: количество матчей в госте
    :return: количество ставок в случае ошибки в госте, иначе список ставок игрока
    """
    bets_array = find_bet(text)
    array = []
    error = False
    length = len(bets_array)
    if count <= length:
        for i in range(count):
            array.append(bets_array[i])
        for i, missing_match in enumerate(missing):
            if missing_match:
                array[i] = 'None'
    else:
        k = 0
        for i, missing_match in enumerate(missing):
            if missing_match:
                array.append('None')
            else:
                if k >= length:
                    error = True
                    break
                else:
                    array.append(bets_array[k])
                    k += 1
    if error:
        return length
    else:
        return array


def print_name_error(text: str, file):
    """
    Выводит сообщение об ошибке в имени в файл и в консоль

    :param text: имя (строка)
    :param file: путь к файлу вывода
    """
    print('Undefined name:', text, file=file)
    print('Undefined name:', text)


class BetText:
    def __init__(self, name, text, number):
        """
        Конструктор класса строк с текстом госта, присылаемого игроком

        :param name: название команды
        :param text: текст госта
        :param number: номер окна ввода для данного игрока
        """
        self.name = name
        self.text = text
        self.number = number


class Error:
    def __init__(self, name, number):
        """
        Конструктор класса сообщений о недостаточном числе ставок в госте

        :param name: название команды
        :param number: количество ставок в госте
        """
        self.name = name
        self.number = number


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        """
        Конструктор класса диалоговых окон без значка справки
        """
        super(Dialog, self).__init__()
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Конструктор класса главного окна
        """
        super(Window, self).__init__()
        self.ui = Ui_MainWindow(self)
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
            print(self.save_scores(), file=saved)
            for bet_text in self.bet_texts:
                text = check_ascii(bet_text.text.toPlainText())
                print(bet_text.name, file=saved)
                print(text, file=saved)
                print(end_symbol, file=saved)
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
            bets = config_bets_array(text, missing)
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
                    count = f'({error.number} став'
                    count += ending_ka(error.number)
                    print('Ошибка в госте:', error.name, count, file=output)

    def config_matches(self):
        """
        Показывает окно настройки матчей
        """
        self.matches.show()

    def config_teams(self):
        """
        Показывает окно настройки названий команд
        """
        self.teams.show()

    def config_settings(self):
        """
        Показывает окно настроек
        """
        self.settings.show()

    def set_names(self, name_array, player_name_array):
        """
        Устанавливает названия команд на экране, определяет список объектов класса BetText с текстами гостов

        :param name_array: список названий команд
        :param player_name_array: список имён игроков
        """
        for i, elem in enumerate(name_array):
            self.ui.box_list[i].name.setText(player_name_array[i])
            self.bet_texts.append(BetText(elem, self.ui.box_list[i].text, i + 1))

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
                    array[i] = self.ui.box_list[bet_text.number - 1].checks[i].isChecked()
        return array

    def open_saves(self):
        """
        Открывает сохранённые данные из файлов
        """
        with open(saved_txt, 'r') as saved:
            saves = saved.readlines()
            saves_text = [get_rid_of_slash_n(saves[i]) for i, line in enumerate(saves)]
            self.open_scores(saves_text)
            i = 0
            while i < len(saves_text):
                j = 1
                for bet_text in self.bet_texts:
                    if bet_text.name == saves_text[i]:
                        text = ''
                        while saves_text[i + j] != end_symbol:
                            if text != '':
                                text += '\n'
                            text += saves_text[i + j]
                            j += 1
                        self.ui.box_list[bet_text.number - 1].text.setPlainText(text)
                i += j
        self.open_checks()

    def open_checks(self):
        """
        Открывает сохранённые данные о нажатых галочках из файла
        """
        with open(checks_txt, 'r') as checks:
            text = checks.readlines()
            for i in range(player_count):
                for j in range(match_count):
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
            scores.append([check_ascii(self.ui.scores[i][0].text()), check_ascii(self.ui.scores[i][1].text())])
            if scores[i][0] in none or scores[i][1] in none:
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
                score[j] = check_ascii(self.ui.scores[i][j].text())
            text += score[0] + '\n' + score[1] + '\n'
        text += end_symbol + '\n'
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

    def set_scores(self, line_array):
        """
        Выводит на экран сохранённые счета матчей

        :param line_array: список счетов матчей (по 1 числу в каждой строке, на 1 матч должно выделяться 2 строки)
        """
        if len(line_array) == match_count * 2:
            for i in range(match_count):
                for j in range(2):
                    self.ui.scores[i][j].setText(get_rid_of_slash_n(line_array[2 * i + j]))

    def open_scores(self, text: list):
        """
        Считывает сохранённые счета матчей из файла.
        В случае несоответствия количества счетов выводит количество строк в сохранённом файле
        """
        score_array = []
        i = 0
        if len(text) > 0:
            while text[i] != end_symbol:
                score_array.append(text[i])
                i += 1
        if len(score_array) == 2 * match_count:
            self.set_scores(score_array)
        else:
            print(len(score_array))


class Matches(Dialog):
    def __init__(self):
        """
        Конструктор класса окна настройки матчей
        """
        super(Matches, self).__init__()
        self.ui = Ui_Dialog(self)
        self.config_teams(self.read_teams())
        self.set_names()
        self.ui.buttonBox.accepted.connect(self.save)
        self.setWindowTitle('Настройка матчей')

    def save(self):
        """
        Сохраняет данные о матчах в файл, вызывается при нажатии на кнопку "Сохранить"
        """
        self.save_matches(matches_txt)

    def save_matches(self, file):
        """
        Сохраняет данные о матчах в файл, создаёт сообщение об ошибке в случае

        :param file: путь к файлу
        """
        text = ''
        for i in range(int(player_count / 2)):
            name = [''] * 2
            for j in range(2):
                name[j] = self.ui.teams[i][j].currentText()
            if text != '':
                text += '\n'
            text += name[0] + ' - ' + name[1]
        with open(file, 'w') as matches:
            print(text, file=matches, end='')

    def check_repeats(self):
        """
        Проверяет наличие повторяющихся команд в настроенном расписании

        :return: True, если повторения есть, False иначе
        """
        teams = [''] * player_count
        array = self.read_matches()
        for i in range(int(player_count / 2)):
            for j in range(2):
                teams[2 * i + j] = array[i][j]
        return False if len(set(teams)) == player_count else True

    @staticmethod
    def read_teams():
        """
        Считывает названия команд из файла

        :return: список названий команд
        """
        with open(players_txt, 'r') as players:
            text = players.readlines()
            names = [split(line, ' - ')[0] for line in text]
        return names

    @staticmethod
    def read_matches():
        """
        Считывает матчи из файла

        :return: список матчей (каждый элемент списка - список из двух названий команд)
        """
        with open(matches_txt, 'r') as matches:
            text = matches.readlines()
            matches = [split(line, ' - ') for i, line in enumerate(text)]
        return matches

    def config_teams(self, names):
        """
        Обновляет выпадающий список команд в окне настройки матчей

        :param names: список названий команд
        """
        for i in range(int(player_count / 2)):
            for j in range(2):
                self.ui.teams[i][j].addItems(names)

    def set_names(self):
        """
        Устанавливает нужные названия команд из списка в соответствии с сохранёнными данными в файле
        """
        matches = self.read_matches()
        for i in range(int(player_count / 2)):
            index = [0] * 2
            for j in range(2):
                index[j] = self.ui.teams[i][j].findText(matches[i][j])
                self.ui.teams[i][j].setCurrentIndex(index[j])


class Teams(Dialog):
    def __init__(self):
        """
        Конструктор класса окна настройки названий команд
        """
        super(Teams, self).__init__()
        self.ui = Ui_Dialog_2(self)
        self.set_names()
        self.ui.buttonBox.accepted.connect(self.save)
        self.setWindowTitle('Настройка команд')

    def save(self):
        """
        Сохраняет названия команд и имена игроков в файл
        :return:
        """
        text = self.save_players()
        with open(players_txt, 'w') as players:
            print(sort_lines_alphabetical(text), file=players, end='')

    def save_players(self):
        """
        Возвращает строку с названиями команд в формате Команда - Имя, разделённые символом "\n"
        """
        text = ''
        for i in range(player_count):
            name = [''] * 2
            name[0] += self.ui.teams[i].text()
            name[1] += self.ui.names[i].text()
            if text != '':
                text += '\n'
            text += name[0] + ' - ' + name[1]
        return text

    def set_names(self):
        """
        Считывает из файла и выводит названия команд и имена игроков
        """
        with open(players_txt, 'r') as players:
            text = players.readlines()
            for i in range(player_count):
                (team, name) = split(text[i], ' - ')
                self.ui.teams[i].setText(team)
                self.ui.names[i].setText(name)


class Results(Dialog):
    def __init__(self):
        """
        Конструктор класса окна с итогами матчей
        """
        super(Results, self).__init__()
        self.ui = Ui_Dialog_3(self)
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
        clipboard = QtWidgets.QApplication.clipboard()
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


class Settings(Dialog):
    def __init__(self):
        """
        Конструктор класса окна с итогами матчей
        """
        super(Settings, self).__init__()
        self.ui = Ui_Dialog_4(self)
        self.setWindowTitle('Настройки')


def main():
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
