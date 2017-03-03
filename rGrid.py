# -*- coding: utf-8 -*-
import config
import words

d = words.Words()


class Grid(object):
    """Работа с сеткой кроссворда

    Parameters
    ----------
    grid: Модель сетки
    """

    insertedList = []  # Слово, строка, столбец, верт/гориз

    def __init__(self, grid):
        super(Grid, self).__init__()
        self.grid = grid
        self.canvas = grid

    def show_canvas(self):
        """Показать изначальную сетку"""

        canvas = self.canvas
        for i in canvas:
            print(i)

    def show(self):
        """Показать сетку"""

        grid = self.grid
        for i in grid:
            print(i)

    def cell(self, row, col):
        return self.grid[row][col]

    def reverse(self, grid):
        """Транспонировать матрицу (сетку)"""

        gridRev = [[j[i] for j in grid]
                   for i in range(len(grid))]
        for i in range(len(gridRev)):
            gridRev[i] = ''.join(gridRev[i])

        return gridRev

    def add_word_to_inserted(self, word, row, col, rev):
        """Добавить слово в insertedList"""

        self.insertedList.append([word, row, col, rev])

    def update_grid(self):
        """Заново отрисовать сетку по insertedList"""

        for w in self.insertedList:
            self.add_word_to_pos(w[0], w[1], w[2], w[3])

    def word_info(self, word):
        """Получить слово, координаты и направление"""

        for elem in self.insertedList:
            if elem[0] == word:
                return elem


grid = Grid(config.file_to_list(config.rgridFilePath))
