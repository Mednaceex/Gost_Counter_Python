from modules.text_functions import split
from modules.classes import Better, League


def get_players(file, league: League):
    """
    Считывает названия команд и имена тренеров из файла, создаёт список объектов класса Better с этими данными

    :param file: путь к файлу
    :param league: лига игрока
    :return: список объектов класса Better
    """
    array = []
    text = file.readlines()
    for line in text:
        a = split(line, ' - ')
        b = Better(league, a[0])
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
