# -*- coding: utf-8 -*-
import codecs

gridFilePath = "grid.txt"
rgridFilePath = "rgrid.txt"

listFilePath = "list.txt"
sortedListFilePath = "listsorted(1).txt"
dictFilePath = "dict.txt"

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
