from modules.const import numbers


def check_ascii(string: str):
    """
    Исключает из строки все символы, не являющиеся символами с номером 32-127 в таблице ASCII или символом '—'

    :param string: строка
    :return: новая строка
    """
    new_string = ''
    for char in string:
        if 31 < ord(char) < 128 or ord(char) == 8212:
            new_string += char
    return new_string


def check_ascii_russian(string: str):
    """
    Исключает из строки все символы, не являющиеся символами с номером 32-127 в таблице ASCII или русскими буквами

    :param string: строка
    :return: новая строка
    """
    new_string = ''
    for char in string:
        if 31 < ord(char) < 128 or 1039 < ord(char) < 1104 or ord(char) in (1025, 1105, 8212):
            new_string += char
    return new_string


def change_space_to_underscore(string: str):
    """
    Заменяет пробелы в строке подчёркиваниями

    :param string: строка
    :return: обработанная строка
    """
    return string.replace(' ', '_')


def change_underscore_to_space(string: str):
    """
    Заменяет подчёркивания в строке пробелами

    :param string: строка
    :return: обработанная строка
    """
    return string.replace('_', ' ')


def check_numbers(string: str):
    """
    Исключает из строки все символы, не являющиеся цифрами

    :param string: строка
    :return: новая строка
    """
    new_string = ''
    for char in string:
        if char in numbers:
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
        return 'ок'
    elif number % 10 == 1:
        return 'ка'
    elif 2 <= number % 10 <= 4:
        return 'ки'
    else:
        return 'ок'


def remove_final_empty_lines(text: str):
    """
    Убирает пустые строки из конца текста

    :param text: текст (строка)
    :return: обработанный текст
    """
    if text:
        while text[-1] == '\n':
            text = text[:-1]
    return text


def get_data(text: list[str], parameter: str, sep='='):
    """
    Получает значение из текста, в каждой строчке которого данные имеют вид "параметр=значение"

    :param text: текст (список строк)
    :param parameter: параметр, значение которого требуется получить
    :param sep: символ, разделяющий значение и параметр в строке
    :return: значение параметра (строка)
    """
    for line in text:
        lst = split(line, sep)
        if lst[0] == parameter:
            return lst[1]
    raise MissingParameterError()


class MissingParameterError(Exception):
    def __init__(self):
        """
        Конструктор класса ошибок при попытке извлечь значение параметра из текста, в котором его нет
        """
        super(MissingParameterError, self).__init__("Ошибка: указанный параметр не найден")
