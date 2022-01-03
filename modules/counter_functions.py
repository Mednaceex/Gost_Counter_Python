from modules.const import numbers, none, long_seps, seps
from modules.text_functions import split
from modules.classes import Better
from modules.custom_config import match_count


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

    :param text: Текст госта (строка)
    :return: Список найденных ставок, каждый элемент которого - список из 2 чисел - ставок на 1 и 2 команды
    """
    for string in long_seps:
        text = text.replace(string, ':')
    for string in seps:
        text = text.replace(string, ':')
    return bets_from_text(text)


def config_bets_list(text: str, missing: list, count=match_count):
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
