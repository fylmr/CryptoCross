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


def show_grid(grid):
    for i in grid:
        print(i)


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

    for line in grid:
        count = 0
        for i in line:
            if count > res:
                res = count
            if i != '_':
                count = 0
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


def insert_word(grid, posX, posY):
    """
    Вставить слово в сетку. Возвращает изменённую сетку

    Args
    grid : list
    posX : int
    posY : int

    Returns
    grid : list
    """


def insert_word_pos(grid):
    """
    Найти наилучшую позицию для вставки слова

    Arguments:
    grid : list

    Returns:
    row, col, length : int
        Где вставлять слово
    """
    rev = False
    if find_max_space(grid)[0] >= find_max_space(grid)[1]:
        length = find_max_space(grid)[0]

        if length < 2:
            raise ValueError("Got word with length < 2")

        pos = insert_word_h_pos(grid, length)
    else:
        gridReversed = [[j[i] for j in grid]
                        for i in range(len(grid))]  # Transpose
        rev = True

        length = find_max_space(grid)[1]
        pos = insert_word_h_pos(gridReversed, length)
    return pos, rev, length


def insert_word_h_pos(grid, length):
    """
    Вставить слово по горизонтали

    Arguments:
    grid : list
    length : int

    Returns:
    row, col : int
        Где вставлять слово
    """

    for row in range(len(grid)):
        count = 0
        for col in range(len(grid)):
            if grid[row][col] != "#":
                count += 1
            if count == length:
                return row, col - length + 1
            else:
                if grid[row][col] != "#":
                    pass
                else:
                    count = 0


grid = file_to_list(config.gridFilePath)
dictList = file_to_list(config.sortedListFilePath)

print(insert_word_pos(grid))
