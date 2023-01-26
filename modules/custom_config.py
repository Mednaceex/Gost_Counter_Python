from modules.paths import custom_txt
from modules.text_functions import split


def get_custom_data():
    """
    Находит пользовательские настройки в файле

    :return: Словарь значений
    """
    with open(custom_txt, 'r') as custom:
        text = custom.readlines()
    d = {}
    for line in text:
        lst = split(line, '=')
        (param, value) = lst
        d[param] = value
    return d


def get_int_data(txt: str):
    """
    Находит пользовательское значение настройки, имеющей целочисленное значение, в файле

    :param txt: название настройки
    :return: значение настройки
    """
    with open(custom_txt, 'r') as custom:
        text = custom.readlines()
    for line in text:
        lst = split(line, '=')
        if lst[0] == txt:
            return int(lst[1])


def get_bool_data(txt: str):
    """
    Находит пользовательское значение настройки, имеющей только булевы значения, в файле

    :param txt: название настройки
    :return: булева переменная
    """
    with open(custom_txt, 'r') as custom:
        text = custom.readlines()
    for line in text:
        lst = split(line, '=')
        if lst[0] == txt:
            return lst[1] == "True"


def get_has_additional():
    """
    Находит пользовательское значение настройки наличия дополнительной ставки в файле

    :return: булева переменная - наличие дополнительной ставки
    """
    return get_bool_data('has_additional')


def get_player_count():
    """
    Находит пользовательское значение количества игроков в файле

    :return: количество игроков
    """
    return get_int_data('player_count')


def get_match_count():
    """
    Находит пользовательское значение количества матчей в файле

    :return: количество матчей
    """
    return get_int_data('match_count')


def get_auto_update():
    """
    Находит пользовательское значение настройки автообновлений в файле

    :return: булева переменная - наличие автоообновлений
    """
    return get_bool_data('auto_update')
