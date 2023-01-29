from modules.const import numbers, long_seps, seps
from modules.text_functions import split
from modules.classes import Better, BetResult, AddBetResult, Result
from modules.custom_config import get_match_count, get_has_additional
from modules.paths import errors_txt


def count_bet(bet1: int, bet2: int, score1: int, score2: int):
    """
    Определяет результат конкретной ставки

    :param bet1: инд. тотал 1 команды в ставке
    :param bet2: инд. тотал 2 команды в ставке
    :param score1: реальный инд. тотал 1 команды
    :param score2: реальный инд. тотал 2 команды
    :return: объект класса BetResult с результатами ставки
    """
    winner = (((bet1 < bet2) and (score1 < score2))
              or ((bet1 > bet2) and (score1 > score2))
              or ((bet1 == bet2) and (score1 == score2)))
    diff = (score2 - score1) == (bet2 - bet1)
    exact = (bet1 == score1) and (bet2 == score2)
    return BetResult(winner, diff, exact)


def count_additional(bet: bool, result: bool):
    """
    Определяет и возвращает количество голов, забитых на дополнительной ставке

    :param bet: дополнительная ставка
    :param result: реальный результат
    """
    return AddBetResult((bet == result) & (result != 'None'))


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


def count_all_bets(name, bets_list, scores_list, betters_list, add_bet=None, add_score=None):
    """
    Определяет результаты всех ставок игрока

    :param name: название команды
    :param bets_list: список ставок игрока
    :param scores_list: список счетов реальных матчей
    :param betters_list: список игроков (объектов класса Better)
    :param add_bet: дополнительная ставка
    :param add_score: исход дополнительной ставки
    """
    results_list = []
    bets = ['None'] * (get_match_count() + int(get_has_additional()))
    for i, bet in enumerate(bets_list):
        if bet == '':
            bets[i] = 'None'
        else:
            bets[i] = bet
    for i, bet in enumerate(bets):
        if bet != 'None' and scores_list[i] != 'None':
            results_list += [count_bet(int(bet[0]), int(bet[1]), int(scores_list[i][0]), int(scores_list[i][1]))]
        else:
            results_list += [Result(valid=False)]
    if get_has_additional():
        results_list[get_match_count()] = count_additional(add_bet, add_score)
    set_player_results(betters_list, name, results_list)


def set_player_results(betters_list, name, results_list):

    for i in betters_list:
        if i.name == name:
            i.set_results(results_list)


def count_score(results_team1: list[Result], results_team2: list[Result], field_factor: bool, count):
    """
    Рассчитывает счёт в матче по спискам результатов каждой ставки
    :param results_team1: список результатов ставок первой команды (объектов класса Result)
    :param results_team2: список результатов ставок второй команды (объектов класса Result)
    :param field_factor: наличие или отсутствие фактора домашнего поля
    :param count: количество матчей в госте
    :return: счёт в матче (кортеж из двух значений - итоговое количество голов каждой команды)
    """
    score1 = 0
    score2 = 0
    for i in range(count):
        if results_team1[i].exact:
            if not results_team2[i].exact or field_factor:
                score1 += 1
            if not results_team2[i].winner:
                score1 += 1
        elif results_team2[i].exact:
            score2 += 1
            if not results_team1[i].winner:
                score2 += 1
        elif results_team1[i].winner and not results_team2[i].winner:
            score1 += 1
        elif not results_team1[i].winner and results_team2[i].winner:
            score2 += 1

    if get_has_additional():
        if results_team1[count].result and not results_team2[count].result:
            score1 += 1
        if not results_team1[count].result and results_team2[count].result:
            score2 += 1
    return score1, score2


def get_match(match: list[str, str], output_file, betters_list: list[Better], field_factor: bool):
    """
    Считывает матч из строки расписания и выводит его счёт в файл вывода

    :param match: матч в формате списка из двух строк - названий команд
    :param field_factor: наличие фактора домашнего поля
    :param betters_list: список игроков (объектов класса Better)
    :param output_file: путь к файлу вывода
    """
    results = [[]] * 2
    name = [''] * 2
    for better in betters_list:
        for k in range(2):
            if better.name == match[k]:
                results[k] = better.results
                name[k] = better.name
    print_match_score(results[0], results[1], name[0], name[1], field_factor, output_file)


def print_match_score(results_team1, results_team2, name_team1, name_team2, field_factor, output_file):
    """
    Считает и выводит счёт матча из строки расписания в файл вывода, проверяет на случай технического поражения или
    ничьей при ошибках в количестве ставок, выводит сообщение об ошибке в случае недостатка указанных команд

    :param results_team1: список результатов первой команды (объектов класса Result)
    :param results_team2: список результатов первой команды (объектов класса Result)
    :param name_team1: название первой команды
    :param name_team2: название первой команды
    :param field_factor: наличие фактора домашнего поля
    :param output_file: путь к файлу вывода
    """
    try:
        print_match_score_to_file(results_team1, results_team2, name_team1, name_team2, field_factor, output_file)
    except IndexError:
        with open(errors_txt, 'w') as error_file:
            print("Ошибка - недостаточно команд указано", file=error_file)


def print_match_score_to_file(results_team1, results_team2, name_team1, name_team2, field_factor, output_file):
    """
    Считает и выводит счёт матча из строки расписания в файл вывода, проверяет на случай технического поражения или
    ничьей при ошибках в количестве ставок

    :param results_team1: список результатов первой команды (объектов класса Result)
    :param results_team2: список результатов первой команды (объектов класса Result)
    :param name_team1: название первой команды
    :param name_team2: название первой команды
    :param field_factor: наличие фактора домашнего поля
    :param output_file: путь к файлу вывода
    """
    if valid(results_team1):
        if valid(results_team2):
            score = count_score(results_team1, results_team2, field_factor, get_match_count())
            print(name_team1, f'{score[0]}-{score[1]}', name_team2, file=output_file)
        else:
            print(name_team1, '3-0', name_team2, '(Тех.)', file=output_file)
    else:
        if valid(results_team2):
            print(name_team1, '0-3', name_team2, '(Тех.)', file=output_file)
        else:
            print(name_team1, '0-0', name_team2, '(Тех.)', file=output_file)


def valid(lst: list[Result]):
    for i in lst:
        if i.valid:
            return True
    return False


def bets_from_text(text: str):
    """
    Ищет ставки игрока, разделённые символом ":", в тексте госта и возвращает список с ними

    :return: Список найденных ставок, каждый элемент которого - список из 2 чисел - ставок на 1 и 2 команды
    """
    array = []
    for i, character in enumerate(text):
        if character == ':' and 0 < i < len(text) - 1:
            if text[i - 1] in numbers and text[i + 1] in numbers:
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

    :param text: Текст госта (строка)
    :return: Список найденных ставок, каждый элемент которого - список из 2 чисел - ставок на 1 и 2 команды
    """
    for string in long_seps:
        text = text.replace(string, ':')
    for string in seps:
        text = text.replace(string, ':')
    return bets_from_text(text)


def check_for_no_errors(text: str, missing: list, count):
    """
    Проверяет текст госта, присланного игроком, на наличие ошибок в количестве ставок

    :param text: текст госта
    :param missing: список из count элементов - True (ставка отсутствует) или False (ставка есть)
    :param count: количество матчей в госте
    :return: True в случае правильного госта, False при наличии ошибок
    """
    num = len(find_bet(text))
    return num == count - missing.count(True) or num == count


def config_bets_list(text: str, missing: list, count):
    """
    Считывает ставки из текста госта, присланного игроком

    :param text: текст госта
    :param missing: список из count элементов - True (ставка отсутствует) или False (ставка есть)
    :param count: количество матчей в госте
    :return: список ставок игрока
    """
    if not check_for_no_errors(text, missing, count):
        raise
    bets_array = find_bet(text)
    array = []
    k = 0
    long = not len(find_bet(text)) == count - missing.count(True)
    for i, missing_match in enumerate(missing):
        if missing_match:
            array.append('None')
            if long:
                k += 1
        else:
            array.append(bets_array[k])
            k += 1
    return array
