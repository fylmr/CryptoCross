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

    def space_pos(self, length=None, rev=False, verbose=False):
        """Возвращает место, в котором будет точно length свободных клеток

        Parameters
        ----------
        length=None
        rev=False
        verbose=False

        Returns
        -------
        row, col
            Если был задан rev, возвращает col, row
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
                else:
                    count = 0
                if count == length:
                    if col + 1 == len(grid) or grid[row][col + 1] == "#":
                        return row, col - length + 1

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
            Формат: [слово, буква]
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

    def letterPositions(self, word, letter):
        res = []
        for lePos in range(len(word)):
            if word[lePos] == letter:
                res.append(lePos)
        return res

    def isIntersectable(self, word, commonList):
        for intersection in commonList:
            for interLetterPos in self.letterPositions(intersection[0],
                                                       intersection[1]):
                pass

    def get_maxdir(self):
        if self.find_max_space(rev=False) > self.find_max_space(rev=True):
            return False
        else:
            return True

    def insert_first(self, maxdir, verbose=True):
        word = self.get_word(self.find_max_space(rev=maxdir))
        maxpos = self.space_pos(rev=maxdir)
        self.add_word_to_pos(word, maxpos[0], maxpos[1], maxdir)

        if verbose:
            print("Word found:", word)
            print("maxpos found")
            print("Added first word to inserted list")
            grid.show()
            print("\n")

        return word

    def creationLoop(self, firstWord, firstDir, verbose=False):
        print("Liftoff")
        counter = 0
        while True:
            if verbose:
                print("\nTRY", counter)

            w = self.get_word(length=random.randint(3, len(firstWord)))
            common = self.common_letters_words(w, firstDir)
            if verbose:
                print("insertedList:", self.insertedList)

            if len(common) > 0:
                if verbose:
                    print("Common words found")

                if self.isIntersectable(w, common):
                    # self.intersect()
                    pass

            else:
                if verbose:
                    print("No common words found")

                if self.space_pos(rev=False, length=len(w)):
                    if verbose:
                        print("Можно вставить по горизонтали")

                    p = self.space_pos(rev=False, length=len(w))
                    self.add_word_to_pos(w, p[0], p[1], False)

                    print("\n")
                    self.show()

                elif self.space_pos(rev=True, length=len(w)):
                    if verbose:
                        print("Можно вставить по вертикали")
                    p = self.space_pos(rev=True, length=len(w))

                    self.add_word_to_pos(w, p[0], p[1], True)

                    print("\n")
                    self.show()

            counter += 1

    def create(self, verbose=False):
        # Ищем максимальное место
        maxdir = self.get_maxdir()

        # Находим подходящее под место первое слово и ставим его
        word = self.insert_first(maxdir)

        # Ищем остальные слова
        self.creationLoop(word, maxdir, verbose)


grid = config.file_to_list(config.gridFilePath)
wordList = config.file_to_list(config.sortedListFilePath)

grid = Grid(grid, wordList)

grid.create(verbose=False)
