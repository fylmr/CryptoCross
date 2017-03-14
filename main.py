# -*- coding: utf-8 -*-
import config
import words
import logging


class Grid(object):
    """Работа с сеткой объекта"""

    def __init__(self, grid, verbose=logging.CRITICAL):
        super(Grid, self).__init__()
        self.grid = grid
        self.canvas = grid[:]
        self.insertedList = []

        logging.basicConfig(
            format=u'[%(lineno)d:%(levelname)s]: %(message)s',
            level=verbose)

    def show(self, canvas=False):
        """Показать рабочую сетку или холст"""
        if canvas:
            grid = self.canvas
        else:
            grid = self.grid
        for i in grid:
            print(i)

    def reverse(self, grid):
        """Транспонировать матрицу (сетку)"""

        gridRev = [[j[i] for j in grid]
                   for i in range(len(grid))]
        for i in range(len(gridRev)):
            gridRev[i] = ''.join(gridRev[i])

        return gridRev


d = words.Words()
grid = Grid(config.file_to_list(config.gridPath), logging.INFO)
print(d.get_word_len(11))
