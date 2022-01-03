def check_ascii(string: str):
    """
    Исключает из строки все символы, не входящие в первые 127 символов таблицы ASCII или не являющиеся символом '—'

    :param string: строка
    :return: новая строка
    """
    new_string = ''
    for char in string:
        if 0 < ord(char) < 128 or ord(char) == ord('—'):
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
