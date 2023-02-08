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
    """
    Возвращает путь к файлу настроек по умолчанию
    """
    return Path('data', 'default_settings.txt')


def get_current_league_txt():
    """
    Возвращает путь к файлу с текущей лигой
    """
    return Path('data', 'current.txt')


def get_leagues_txt():
    """
    Возвращает путь к файлу со списком лиг
    """
    return Path('data', 'leagues.txt')


def rename_folder(old_name: str, new_name: str):
    """
    Переименовывает папку в директории "data/leagues"
    :param old_name: текущее имя папки
    :param new_name: новое имя папки
    """
    p = Path('data', 'leagues', old_name)
    p.rename(Path('data', 'leagues', new_name))


def delete_league_folder(league_folder_name):
    """
    Удаляет папку лиги
    :param league_folder_name: название папки лиги
    """
    p = Path('data', 'leagues', league_folder_name)
    rmtree(p)


def init_league(league_folder_name: str):
    """
    Создаёт папку лиги со всеми файлами
    
    :param league_folder_name: название папки лиги
    :return:
    """
    p = Path('data', 'leagues', league_folder_name)
    p.mkdir()
    for file_name in ['additional.txt', 'checks.txt', 'scores.txt', 'custom.txt', 'errors.txt', 'matches.txt',
                      'saved.txt', 'output.txt', 'players.txt']:
        with open(get_path(league_folder_name, file_name), 'w+'):
            pass
