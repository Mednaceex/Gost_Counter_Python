from modules.paths import get_current_league_txt, get_default_settings_txt, get_leagues_txt
from modules.text_functions import get_data, get_rid_of_slash_n, change_underscore_to_space
from modules.classes import League


def get_current_league():
    """
    Находит в файле название установленной на данный момент лиги

    :return: Название лиги
    """
    file = get_current_league_txt()
    with open(file, encoding='utf-8', mode='r') as current:
        text = current.readlines()
    return get_data(text, "league")


def get_default_int_data(setting: str):
    """
    Находит значение настройки, имеющей целочисленное значение, в файле default_settings.txt

    :param setting: название настройки
    :return: значение настройки
    """
    with open(get_default_settings_txt(), 'r') as default:
        text = default.readlines()
    return int(get_data(text, setting))


def get_default_bool_data(setting: str):
    """
    Находит значение настройки, имеющей булево значение, в файле default_settings.txt

    :param setting: название настройки
    :return: значение настройки
    """
    with open(get_default_settings_txt(), 'r') as default:
        text = default.readlines()
    return get_data(text, setting) == "True"


def get_max_player_count():
    """
    Находит значение максимально возможного количества игроков в файле

    :return: количество игроков
    """
    return get_default_int_data('max_player_count')


def get_max_match_count():
    """
    Находит значение максимально возможного количества матчей в файле

    :return: количество матчей
    """
    return get_default_int_data('max_match_count')


def get_leagues():
    """
    Считывает названия лиг из файла

    :return: список из названий лиг
    """
    with open(get_leagues_txt(), encoding='utf-8', mode='r') as leagues:
        text = leagues.readlines()

    # Убирает все пустые строки
    return list(filter(lambda x: x != '', [change_underscore_to_space(get_rid_of_slash_n(line)) for line in text]))


def save_leagues(league_list: list[str]):
    """
    Сохраняет названия лиг в файл

    :param league_list: список из названий лиг
    """
    with open(get_leagues_txt(), encoding='utf-8', mode='w') as leagues:
        for league in league_list:
            print(f'{league}', file=leagues)


def save_current_league(league_name: str):
    """
    Сохраняет название текущей лиги в файл

    :param league_name: название лиг
    """
    with open(get_current_league_txt(), encoding='utf-8', mode='w') as current:
        print(f'league={change_underscore_to_space(league_name)}', file=current)


def set_default_settings(league_name: str):
    """
    Задаёт настройки по умолчанию в данной лиге

    :param league_name: название лиги
    """
    match_count = get_default_int_data('match_count')
    player_count = get_default_int_data('player_count')
    has_additional = get_default_bool_data('has_additional')
    auto_update = get_default_bool_data('auto_update')
    text = 'player_count=' + str(player_count) + '\nmatch_count=' +\
           str(match_count) + '\nhas_additional=' + str(has_additional) + '\nauto_update=' + str(auto_update)
    with open(League(league_name).get_custom_txt(), 'w') as custom:
        print(text, file=custom)


def init_files(league_name: str):
    """
    Создаёт необходимые файлы для создания данной лиги

    :param league_name: название лиги
    """
    with open(League(league_name).get_additional_txt(), 'w') as add:
        print('None\n', file=add)
