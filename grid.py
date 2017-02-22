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

    insertedList = []  # Слово, строка, столбец, вертикаль?

    def __init__(self, grid, wordList):
        super(Grid, self).__init__()
        self.grid = grid
        self.canvas = grid
        self.wordList = wordList

    def show(self):
        """Показать сетку
        """

        grid = self.grid
        for i in grid:
            print(i)

    def showCanvas(self):
        """Показать изначальную сетку
        """

        canvas = self.canvas
        for i in canvas:
            print(i)

    def reverse(self, grid):
        """Транспонировать матрицу (сетку)
        """
        gridRev = [[j[i] for j in grid]
                   for i in range(len(grid))]
        for i in range(len(gridRev)):
            gridRev[i] = ''.join(gridRev[i])

        return gridRev

    def add_word_to_insertedlist(self, word, col, row, rev):
        self.insertedList.append([word, col, row, rev])

    def find_max_space(self, rev=False):
        """Максимальная длина места, в котором нет чёрных клеток

        Parameters
        ----------
        rev=False: bool
            Смотреть по вертикали
        Returns
        -------
        res: int
            Максимальное место по заданному направлению
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
                if i == '#':
                    count = 0
                else:
                    count += 1
            if count > res:
                res = count

        return res

    def get_word(self, length, step=3):
        """Найти слово нужной длины

        Parameters
        ----------
        length: Желаемая длина
        step=3: Шаг поиска

        Returns
        -------
        word: Слово
        """

        wordList = self.wordList

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

        if rev:
            grid = self.reverse(self.grid)
        else:
            grid = self.grid

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

    def add_word_to_pos(self, word, row, col, rev=False):
        """Поставить слово на позицию. Изменяет сетку

        Parameters
        ----------
        word: Слово
        row: Ряд
        col: Столбец
        rev=False: По вертикали?
        """

        if rev:
            grid = self.reverse(self.grid)
            row, col = col, row
        else:
            grid = self.grid

        length = len(word)

        grid[row] = grid[row][:col] + word + grid[row][col + length:]
        # Должна быть проверка, чтоб слово не выходило за пределы экрана

        if rev:
            self.grid = self.reverse(grid)
            row, col = col, row
        else:
            self.grid = grid

        self.add_word_to_insertedlist(word, row, col, rev)

    def common_letters_words(self, word):
        """Вернёт список слов, с которыми есть пересечения в буквах,
        в формате [слово, буква]

        Parameters
        ----------
        word: Слово

        Returns
        -------
        res: Список слов, с которыми есть пересечения
        """

        res = []
        for w in self.insertedList:
            for letter in word:
                if letter in w[0]:
                    res.append([w[0], letter])
                    break
        return res


grid = config.file_to_list(config.gridFilePath)
wordList = config.file_to_list(config.sortedListFilePath)

grid = Grid(grid, wordList)
