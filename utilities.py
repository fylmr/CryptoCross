# -*- coding: utf-8 -*-
import config


def grid_file_to_list(path):
    res = []
    with open(path) as f:
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


def find_word(length):
    """
    Найти слово нужной длины

    Arguments:
    length : int

    Returns:
    word : string
    """


grid = grid_file_to_list(config.gridFilePath)

print(find_max_space(grid))
