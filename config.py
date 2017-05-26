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


def strings_to_file(*strings):
    with open(saveFile, "w") as f:
        for string in strings:
            f.write(string)
            print("\n")


def save(grid, insertedList):
    with open(saveFile, "w") as f:
        for line in grid:
            for symbol in line:
                if symbol in ["0", "1", "2"]:
                    f.write(" ")
                else:
                    f.write(symbol)
            # f.write(line)
            f.write("\n")
        f.write("\n")
        for word in insertedList:
            f.write(str(word[1] + 1))  # Так как нумерация с нуля
            f.write(" ")
            f.write(str(word[2] + 1))
            f.write(" ")
            if word[3] is True:
                f.write("В — ")
            else:
                f.write("Г — ")
            f.write(word[0])
            f.write("\n")
