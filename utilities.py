# -*- coding: utf-8 -*-
import config
import random
import codecs


def file_to_list(path):
    res = []
    with codecs.open(path, 'r', "utf_8_sig") as f:
        res = f.readlines()
    res = [x.strip() for x in res]
    return res


def find_max_space(grid):
    """
    Найти максимальное пустое место

    Arguments:
    grid : list

    Returns:
    resH, resV : int
    """

    resH = find_max_space_h(grid)
    gridReversed = [[j[i] for j in grid]
                    for i in range(len(grid))]  # Transpose
    resV = find_max_space_h(gridReversed)

    return resH, resV


def find_max_space_h(grid):
    res = 0
    # Горизонтальная проверка
    for line in grid:

        # Слева направо
        count = 0
        for i in line:
            if i != '_':
                if count > res:
                    res = count
                count = 0
            else:
                count += 1

        # Справа налево
        count = 0
        for i in reversed(line):
            if i == '#':
                break
            else:
                count += 1
        if count > res:
            res = count

    return res


def find_word(wordList, length):
    """
    Найти слово нужной длины

    Arguments:
    wordList : list
    length : int

    Returns:
    word : string
    """
    step = 5

    n = random.randint(0, len(wordList))
    print(n)
    while len(wordList[n]) != length:
        if len(wordList[n]) > length:
            n += step
        else:
            n -= step
        if n < 0 or n > len(wordList):
            n = random.randint(0, len(wordList))

    return wordList[n]


grid = file_to_list(config.gridFilePath)
wordList = file_to_list(config.sortedListFilePath)

print(find_word(wordList, find_max_space(grid)[1]))
