# -*- coding: utf-8 -*-
import config
import random
# import codecs


class Grid(object):
    """Работа с сеткой кроссворда

    Parameters
    ----------
    grid: Модель сетки
    wordList: Словарь
    """

    def __init__(self, grid, wordList):
        super(Grid, self).__init__()
        self.grid = grid
        self.wordList = wordList

    def show(self):
        """Показать сетку
        """

        grid = self.grid
        for i in grid:
            print(i)

    def reverse(self, grid):
        """Транспонировать матрицу (сетку)
        """
        gridRev = [[j[i] for j in grid]
                   for i in range(len(grid))]
        for i in range(len(gridRev)):
            gridRev[i] = ''.join(gridRev[i])

        return gridRev

    def find_max_space(self, rev=False):
        """Максимальное свободное место

        Parameters
        ----------
        rev=True: bool
            Смотреть по вертикали
        Returns
        -------

        """

        grid = self.grid

        if not rev:
            res = self.find_max_space_h(grid)
        else:
            res = self.find_max_space_h(self.reverse(grid))

        return res

    def find_max_space_h(self, grid):
        """Найти максимальное место в {grid} по горизонтали
        """
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

    def find_word(self, length):
        """Найти слово нужной длины

        Parameters
        ----------
        length: Желаемая длина

        Returns
        -------
        word: Слово
        """

        wordList = self.wordList

        step = 3

        n = random.randint(0, len(wordList))

        while len(wordList[n]) != length:
            if len(wordList[n]) > length:
                n += step
            else:
                n -= step
            if n < 0 or n > len(wordList):
                n = random.randint(0, len(wordList))

        return wordList[n]

    def max_space_pos(self, rev=False, verbose=False):
        """Вернуть координаты максимально пустого места

        Parameters
        ----------
        rev = False: bool
            Вставить по вертикали
        verbose = False: bool
            Показывать процесс
        Returns
        -------
        row, col: int
            Строка и столбец
        """

        grid = self.grid

        length = self.find_max_space()

        for row in range(len(grid)):
            count = 0
            for col in range(len(grid)):
                if grid[row][col] == "_":
                    count += 1
                if count == length:
                    return row, col - length + 1
                else:
                    if grid[row][col] == "_":
                        pass
                    else:
                        count = 0


grid = config.file_to_list(config.gridFilePath)
wordList = config.file_to_list(config.sortedListFilePath)

grid = Grid(grid, wordList)

print(grid.max_space_pos())
