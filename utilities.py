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
    Найти наибольшее пространство, доступное для слова.
    grid - list
    """
    res = 0
    # Горизонтальная проверка
    for line in grid:

        # Слева направо
        count = 0
        for i in line:
            if i == '#':
                break
            else:
                count += 1
        if count > res:
            res = count

        # Справа налево
        count = 0
        for i in reversed(line):
            if i == '#':
                break
            else:
                count += 1
        if count > res:
            res = count

    # Вертикальная проверка
    for i in range(1, len(grid)):
        pass

    return res


grid = grid_file_to_list(config.gridFilePath)

print(find_max_space(grid))
