from pathlib import Path
from shutil import rmtree


def get_path(league_name, file_name):
    """
    Создаёт объект пути к нужному файлу в лиге

    :param league_name: название лиги
    :param file_name: название файла
    :return: путь (объект класса pathlib.Path)
    """
    return Path('data', 'leagues', league_name, file_name)


def get_default_settings_txt():
    return Path('data', 'default_settings.txt')


def get_current_league_txt():
    return Path('data', 'current.txt')


def get_leagues_txt():
    return Path('data', 'leagues.txt')


def rename_folder(old_name: str, new_name: str):
    p = Path('data', 'leagues', old_name)
    p.rename(Path('data', 'leagues', new_name))


def delete_league_folder(league_name):
    p = Path('data', 'leagues', league_name)
    rmtree(p)


def init_league(league_name: str):
    p = Path('data', 'leagues', league_name)
    p.mkdir()
    for file_name in ['additional.txt', 'checks.txt', 'scores.txt', 'custom.txt', 'errors.txt', 'matches.txt',
                      'saved.txt', 'output.txt', 'players.txt']:
        with open(get_path(league_name, file_name), 'w+'):
            pass
