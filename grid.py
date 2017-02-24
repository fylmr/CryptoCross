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

    def add_word_to_insertedlist(self, word, row, col, rev):
        self.insertedList.append([word, row, col, rev])

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

    def max_space_pos(self, rev=False, verbose=False, length=None):
        """Вернуть координаты максимально пустого места

        Parameters
        ----------
        rev = False: bool
            Вставить по вертикали
        verbose = False: bool
            Показывать процесс
        length = None: bool
            Если дать значение, ищет место для нужной длины,
            если оставить — ищет максимально возможное
        Returns
        -------
        row, col: int or None
            Строка и столбец, если найдено место
            или ничего, если места нет
        """

        grid = self.grid

        if length is None:
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

    def exact_space_pos(self, length, rev=False, verbose=False):
        grid = self.grid

        if length is None:
            length = self.find_max_space()

        if rev:
            grid = self.reverse(self.grid)
        else:
            grid = self.grid

        for row in range(len(grid)):
            count = 0
            for col in range(len(grid)):
                if grid[row][col] == "_" and col + 1 < len(grid):
                    count += 1
                else:
                    if count == length:
                        return row, col - length
                    # if grid[row][col] == "_":
                    #     pass
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

    def common_letters_words(self, word, rev=False):
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
                    # if w[3] != rev:
                    #     res.append([w[0], letter])
                    #     break
                    res.append([w[0], letter])
                    break
        return res

    def create(self, verbose=False):

        # Ищем максимальное место
        if self.find_max_space(rev=False) > self.find_max_space(rev=True):
            maxdir = False
        else:
            maxdir = True

        # Находим подходящее под место первое слово
        word = self.get_word(self.find_max_space(rev=maxdir))
        print("Word found:", word)

        maxpos = self.max_space_pos(rev=maxdir)
        print("maxpos found")

        self.add_word_to_pos(word, maxpos[0], maxpos[1], maxdir)
        print("Added first word to inserted list")

        print("Liftoff")
        counter = 0
        while True:
            print("\nTRY", counter)

            w = self.get_word(length=random.randint(3, len(word)))
            common = self.common_letters_words(w, maxdir)
            print("insertedList:", self.insertedList)

            if len(common) > 0:
                pass
                print("Common words found")
            else:
                print("No common words found")

                if self.exact_space_pos(rev=False, length=len(w)):
                    print("Можно вставить по горизонтали")

                    p = self.exact_space_pos(rev=False, length=len(w))
                    self.add_word_to_pos(w, p[0], p[1], False)
                    self.show()

                elif self.exact_space_pos(rev=True, length=len(w)):
                    print("Можно вставить по вертикали")
                    p = self.exact_space_pos(rev=True, length=len(w))

                    self.add_word_to_pos(w, p[0], p[1], True)
                    self.show()

            counter += 1


grid = config.file_to_list(config.gridFilePath)
wordList = config.file_to_list(config.sortedListFilePath)

grid = Grid(grid, wordList)

grid.create(True)
