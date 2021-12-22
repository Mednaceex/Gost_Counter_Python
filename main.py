from PyQt5 import QtWidgets, QtCore
from modules.window import Ui_MainWindow
from modules.matches import Ui_Dialog
from modules.teams import Ui_Dialog as Ui_Dialog_2
from modules.results import Ui_Dialog as Ui_Dialog_3
import sys
from pathlib import Path

none = ('xx', 'хх', 'ХХ', 'XX', '__', '--', '_', '//', '/', '', 'None')
match_count = 10
player_count = 20
long_seps = (' -:- ', '—:—', ' -:-', '-:- ', '-:-')
seps = ('-', '—')
numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
end_symbol = '//'

saved_txt = Path('txt', 'saved.txt')
errors_txt = Path('txt', 'errors.txt')
checks_txt = Path('txt', 'checks.txt')
matches_txt = Path('txt', 'matches.txt')
output_txt = Path('txt', 'output.txt')
players_txt = Path('txt', 'players.txt')


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
    Исключает из строки все символы, не входящие в первые 127 символов таблицы ASCII

    :param string: строка
    :return: новая строка
    """
    new_string = ''
    for char in string:
        if 0 < ord(char) < 128:
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
    array = []
    for better in betters_array:
        array.append(better.name)
    return array


def get_player_names(betters_array):
    """
    Возвращает список названий команд с именами игроков

    :param betters_array: список объектов класса Better
    :return: список названий команд с именами игроков из полученного списка
     Формат строки в списке: Команда (Имя)
    """
    array = []
    for better in betters_array:
        array.append(better.name + ' (' + better.player_name + ')')
    return array


def count_goals(name, bets_list, scores_list, betters_list):
    """
    Рассчитывает количество забитых игроком голов

    :param name: название команды
    :param bets_list: список ставок игрока
    :param scores_list: список счетов матчей
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


def get_matches(line, output_file, betters_list):
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


def find_bet(text: str):
    """
    Ищет ставки игрока в тексте госта, возвращает массив с ними
    Каждый элемент возвращаемого массива - список из 2 чисел - ставок на 1 и 2 команды
    """
    array = []
    for string in long_seps:
        text = text.replace(string, ':')
    for string in seps:
        text = text.replace(string, ':')
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


def config_bets_array(text: str, missing: list, count=match_count):
    """
    Считывает ставки из текста госта, присланного игроком

    :param text: текст госта
    :param missing: массив из count элементов - True (ставка отсутствует) или False (ставка есть)
    :param count: количество матчей в госте
    :return: количество ставок в случае ошибки в госте, иначе массив ставок игрока
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
        Конструктор класса строк с текстом госта, присылаемого ироком

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.matches = Matches()
        self.teams = Teams()
        self.results = Results()
        self.bet_texts = []
        self.score = []
        with open(players_txt, 'r') as players:
            self.betters = get_players(players)
        self.set_names(get_names(self.betters), get_player_names(self.betters))
        self.open_saves()
        self.setWindowTitle('Счётчик гостов')

        self.ui.Matches_Button.clicked.connect(self.config_matches)
        self.ui.Teams_Button.clicked.connect(self.config_teams)
        self.ui.Save_Button.clicked.connect(self.save)
        self.ui.Count_Button.clicked.connect(self.count)
        self.ui.Reset_Button.clicked.connect(self.clear)

    def save(self):
        """
        Созраняет введённые значения в соответствующие файлы
        """
        with open(saved_txt, 'w') as saved:
            print(self.save_scores(), file=saved)
            for bet_text in self.bet_texts:
                text = check_ascii(bet_text.text.toPlainText())
                print(bet_text.name, file=saved)
                print(text, file=saved)
                print(end_symbol, file=saved)
        with open(checks_txt, 'w') as checks:
            check_box = [self.ui.Check_1_1]
            for i in range(player_count):
                for j in range(match_count):
                    exec(f'check_box[{0}] = self.ui.Check_{i + 1}_{j + 1}')
                    if check_box[0].isChecked():
                        print(1, end='', file=checks)
                    else:
                        print(0, end='', file=checks)
                print('', file=checks)

    def count(self):
        """
        Рассчитывает результаты матча и выводит на экран окно с ними
        """
        self.save()
        self.score = self.get_scores()
        errors = []
        for bet_text in self.bet_texts:
            text = check_ascii(bet_text.text.toPlainText())
            missing = self.get_missing(bet_text.name)
            bets = config_bets_array(text, missing)
            if type(bets) is not int:
                count_goals(bet_text.name, bets, self.score, self.betters)
            else:
                for better in self.betters:
                    if better.name == bet_text.name:
                        better.goals = 0
                errors.append(Error(bet_text.name, bets))

        with open(output_txt, 'w+') as output:
            with open(matches_txt, 'r') as matches:
                text = matches.readlines()
                for line in text:
                    if line != '\n':
                        get_matches(line, output, self.betters)

        with open(errors_txt, 'w') as output:
            if errors:
                for error in errors:
                    count = f'({error.number} став'
                    if 5 <= error.number <= 20:
                        count += 'ок)'
                    elif error.number % 10 == 1:
                        count += 'ка)'
                    elif 2 <= error.number % 10 <= 4:
                        count += 'ки)'
                    else:
                        count += 'ок)'
                    print('Ошибка в госте:', error.name, count, file=output)

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

    # noinspection PyMethodMayBeStatic
    def set_names(self, name_array, player_name_array):
        """
        Устанавливает названия команд на экране, определяет список объектов класса BetText с текстами гостов

        :param name_array: список названий команд
        :param player_name_array: список имён игроков
        """
        for i, elem in enumerate(name_array):
            exec(f'self.ui.Name_{i + 1}.setText(player_name_array[{i}])')
            exec(f'self.bet_texts.append(BetText(elem, self.ui.Text_{i + 1}, {i + 1}))')

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
                    exec(f'array[{i}] = self.ui.Check_{bet_text.number}_{i + 1}.isChecked()')
        return array

    def open_saves(self):
        """
        Открывает сохранённые данные из файлов
        """
        with open(saved_txt, 'r') as saved:
            saves = saved.readlines()
            saves_text = []
            for i, line in enumerate(saves):
                saves_text.append(get_rid_of_slash_n(saves[i]))
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
                        number = bet_text.number
                        exec(f'self.ui.Text_{number}.setPlainText(text)')
                i += j
        self.open_checks()

    # noinspection PyMethodMayBeStatic
    def open_checks(self):
        """
        Открывает сохранённые данные о нажатых галочках из файла
        """
        with open(checks_txt, 'r') as checks:
            text = checks.readlines()
            for i in range(player_count):
                for j in range(match_count):
                    if text[i][j] == '1':
                        exec(f'self.ui.Check_{i + 1}_{j + 1}.setCheckState(QtCore.Qt.Checked)')

    # noinspection PyMethodMayBeStatic
    def get_scores(self):
        """
        Считывает счета матчей из полей для ввода

        :return: список счетов матчей
        Каждый элемент возвращаемого списка - список из 2 чисел - ставок на 1 и 2 команды
        """
        scores = ['None'] * match_count
        for i in range(match_count):
            exec(f'scores[{i}] = [check_ascii(self.ui.Score_{i + 1}_1.text()),'
                 f'check_ascii(self.ui.Score_{i + 1}_2.text())]')
            if scores[i][0] in none or scores[i][1] in none:
                scores[i] = 'None'
        return scores

    # noinspection PyMethodMayBeStatic
    def save_scores(self):
        """
        Возвращает счета матчей в текстовом виде для сохранения в файл
        """
        text = ''
        for i in range(match_count):
            score = [''] * 2
            for j in range(2):
                exec(f'score[{j}] = check_ascii(self.ui.Score_{i + 1}_{j + 1}.text())')
            text += score[0] + '\n' + score[1] + '\n'
        text += end_symbol + '\n'
        return text

    # noinspection PyMethodMayBeStatic
    def clear_scores(self):
        """
        Очищает поля для ввода счетов матчей
        """
        empty = ''
        for i in range(match_count):
            for j in range(2):
                exec(f'self.ui.Score_{i + 1}_{j + 1}.setText(empty)')

    # noinspection PyMethodMayBeStatic
    def clear_checks(self):
        """
        Снимает все галочки
        """
        for i in range(player_count):
            for j in range(match_count):
                exec(f'self.ui.Check_{i + 1}_{j + 1}.setCheckState(QtCore.Qt.Unchecked)')

    # noinspection PyMethodMayBeStatic
    def set_scores(self, line_array):
        """
        Выводит на экран сохранённые счета матчей

        :param line_array: список счетов матчей (по 1 числу в каждой строке, на 1 матч должно выделяться 2 строки)
        """
        if len(line_array) == match_count * 2:
            for line in line_array:
                for i in range(match_count):
                    for j in range(2):
                        exec(f'self.ui.Score_{i + 1}_{j + 1}.setText(get_rid_of_slash_n(line_array[2 * i + {j}]))')

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
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.config_teams(self.read_teams())
        self.set_names()
        self.ui.buttonBox.accepted.connect(self.save)
        self.setWindowTitle('Настройка матчей')

    def save(self):
        """
        Сохраняет данные о матчах в файл, вызывается при нажатии на кнопку "Сохранить"
        """
        self.save_matches(matches_txt)

    # noinspection PyMethodMayBeStatic
    def save_matches(self, file):
        """
        Сохраняет данные о матчах в файл
        """
        text = ''
        for i in range(int(player_count / 2)):
            name = [''] * 2
            for j in range(2):
                exec(f'name[{j}] = self.ui.Team_{i + 1}_{j + 1}.currentText()')
            if text != '':
                text += '\n'
            text += name[0] + ' - ' + name[1]
        with open(file, 'w') as matches:
            print(text, file=matches, end='')

    @staticmethod
    def read_teams():
        """
        Считывает названия команд из файла

        :return: список названий команд
        """
        names = []
        with open(players_txt, 'r') as players:
            text = players.readlines()
            for line in text:
                array = split(line, ' - ')
                names.append(array[0])
        return names

    # noinspection PyMethodMayBeStatic
    def config_teams(self, names):
        """
        Обновляет выпадающий список команд в окне настройки матчей
        :param names: список названий команд
        """
        for i in range(int(player_count / 2)):
            for j in range(2):
                exec(f'self.ui.Team_{i + 1}_{j + 1}.addItems(names)')

    # noinspection PyMethodMayBeStatic
    def set_names(self):
        """
        Устанавливает нужные названия команд из списка в соответствии с сохранёнными данными в файле
        """
        with open(matches_txt, 'r') as matches:
            text = matches.readlines()
            for i, line in enumerate(text):
                if i < int(player_count / 2):
                    match = split(line, ' - ')
                    index = [0] * 2
                    for j in range(2):
                        exec(f'index[{j}] = self.ui.Team_{i + 1}_{j + 1}.findText(match[{j}])')
                        exec(f'self.ui.Team_{i + 1}_{j + 1}.setCurrentIndex(index[{j}])')


class Teams(Dialog):
    def __init__(self):
        """
        Конструктор класса окна настройки названий команд
        """
        super(Teams, self).__init__()
        self.ui = Ui_Dialog_2()
        self.ui.setupUi(self)
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

    # noinspection PyMethodMayBeStatic
    def save_players(self):
        """
        Возвращает строку с названиями команд в формате Команда - Имя, разделённые символом "\n"
        """
        text = ''
        for i in range(player_count):
            name = [''] * 2
            exec(f'name[{0}] += self.ui.Team_{i + 1}.text()')
            exec(f'name[{1}] += self.ui.Name_{i + 1}.text()')
            if text != '':
                text += '\n'
            text += name[0] + ' - ' + name[1]
        return text

    # noinspection PyMethodMayBeStatic
    def set_names(self):
        """
        Считывает из файла и выводит названия команд и имена игроков
        """
        with open(players_txt, 'r') as players:
            text = players.readlines()
            for i in range(player_count):
                names = split(text[i], ' - ')
                exec(f'self.ui.Team_{i + 1}.setText(names[0])')
                exec(f'self.ui.Name_{i + 1}.setText(names[1])')


class Results(Dialog):
    def __init__(self):
        """
        Конструктор класса окна с итогами матчей
        """
        super(Results, self).__init__()
        self.ui = Ui_Dialog_3()
        self.ui.setupUi(self)
        self.print_results()
        self.setWindowTitle('Результаты матчей')
        self.show_copied(False)

        self.ui.Copy_Button.clicked.connect(self.copy)
        self.ui.Exit_Button.clicked.connect(self.close)

    def copy(self):
        """
        Копирует текст результатов в буфер обмена, показывает надпись "Скпировано"
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


def main():
    app = QtWidgets.QApplication([])
    application = Window()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
