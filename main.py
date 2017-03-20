# -*- coding: utf-8 -*-
import config
import words
import logging
import os
import time


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

    def get_cell(self, row, col, canvas=False):
        if canvas:
            return self.canvas[row][col]
        else:
            return self.grid[row][col]

    def reverse(self, grid):
        """Транспонировать матрицу (сетку)"""

        gridRev = [[j[i] for j in grid]
                   for i in range(len(grid))]
        for i in range(len(gridRev)):
            gridRev[i] = ''.join(gridRev[i])

        return gridRev

    def add_to_inserted(self, word, row, col, rev):
        """Добавить слово в insertedList"""
        self.insertedList.append([word, row, col, rev])

    def place(self, word, row, col, rev):
        """Поставить слово на позицию. Изменяет сетку

        word: Слово
        row: Ряд
        col: Столбец
        rev: По вертикали?
        """

        if rev:
            grid = self.reverse(self.grid)
            row, col = col, row
        else:
            grid = self.grid

        length = len(word)

        grid[row] = grid[row][:col] + word + grid[row][col + length:]

        if rev:
            self.grid = self.reverse(grid)
            row, col = col, row
        else:
            self.grid = grid

        self.add_to_inserted(word, row, col, rev)

    def plusable(self, grid, row, col):
        if row >= 0 and row < len(grid):
            if col >= 0 and col < len(grid):
                if grid[row][col] != "#":
                    grid[row] = grid[row][:col] + \
                        "+" + grid[row][col + 1:]
                    return True

        return False

    def mark_fragment(self, row, col, get_pluses=False):
        """Площадь фрагмента. Пускается из row, col"""
        grid = self.grid[:]

        pluses = [[row, col]]
        checked = []

        for plus in pluses:
            if plus in checked:
                continue
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j or i == -j:
                        continue
                    if self.plusable(grid, plus[0] + i, plus[1] + j):
                        pluses.append([plus[0] + i, plus[1] + j])
            checked.append(plus)

            # os.system('cls')
            # self.show()
            # print("\n")
            # time.sleep(.05)

        pluses = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == "+":
                    pluses.append([i, j])

        if get_pluses:
            return pluses
        return len(pluses)

    def get_fragmented_rulers(self, row, col, get_length=False):
        res = []
        for f in self.mark_fragment(row, col, True):
            if self.grid[f[0]][f[1]] in ['0', '1', '2']:
                res.append(f)

        if get_length:
            return len(res)
        return res


os.system('cls')

d = words.Words()
grid = Grid(config.file_to_list(config.gridPath), logging.DEBUG)

print(grid.get_fragmented_rulers(1, 0))
