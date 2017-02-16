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
            if i != '_':
                if count > res:
                    res = count
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


def insert_word(grid):
    if find_max_space(grid)[0] >= find_max_space(grid)[1]:
        pos = insert_word_h_pos(grid, find_max_space(grid)[0])
    else:
        pos = insert_word_h_pos(grid, find_max_space(grid)[1])


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
            print(row, col, count)
            if count == length:
                return row, col - length
            else:
                if grid[row][col] != "#":
                    count += 1
                else:
                    count = 0


def show_grid(grid):
    for i in grid:
        print(i)


grid = file_to_list(config.gridFilePath)
wordList = file_to_list(config.sortedListFilePath)

print(insert_word_h_pos(grid, 11))
