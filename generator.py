# -*- coding: utf-8 -*-
import config


def grid_file_to_list(path):
    res = []
    with open(path) as f:
        res = f.readlines()
    res = [x.strip() for x in res]
    return res


def find_max_space():
    """
    Найти наибольшее пространство, доступное для слова.
    """
    pass


grid = grid_file_to_list(config.gridFilePath)
for i in grid:
    print(i)
