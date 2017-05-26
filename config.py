# -*- coding: utf-8 -*-
import codecs

gridPath = "grid_1.txt"
rgridPath = "rgrid.txt"

listPath = "list.txt"
sortedListPath = "listsorted.txt"

saveFile = "save.txt"


def file_to_list(path):
    """Построчно превратить файл в список

    Parameters
    ----------
    path: Путь к файлу

    Returns
    -------
    res: Список
    """

    res = []
    with codecs.open(path, 'r', "utf_8_sig") as f:
        res = f.readlines()
    res = [x.strip() for x in res]
    return res
