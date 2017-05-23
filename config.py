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


def save_grid_to_file(grid, file=saveFile):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] in ["_", "#", "0", "1", "2"]:
                grid[i] = grid[i][:j] + " " + grid[i][j + 1:]

    with codecs.open(file, 'w', "utf_8_sig") as f:
        for i in range(len(grid)):
            f.write(grid[i])
            f.write("\n")
