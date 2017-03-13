# -*- coding: utf-8 -*-
import config
import words
import logging
import random

d = words.Words()


class Grid(object):
    """Работа с сеткой кроссворда

    Parameters
    ----------
    grid: Модель сетки
    """

    insertedList = []  # Слово, строка, столбец, верт/гориз

    def __init__(self, grid, verbose=logging.CRITICAL):
        super(Grid, self).__init__()
        self.grid = grid
        self.canvas = grid

        logging.basicConfig(
            format=u'[%(lineno)d:%(levelname)s]: %(message)s',
            level=verbose)

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
        """Что стоит в клетке?"""

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

        logging.debug("{} added to inserted".format(word))
        self.insertedList.append([word, row, col, rev])

    def update_grid(self):
        """Заново отрисовать сетку по insertedList"""
        logging.debug("grid updated")

        for w in self.insertedList[:]:
            logging.debug("for {} in insertedList".format(w))
            self.add_word_to_pos(w[0], w[1], w[2], w[3])

    def word_info(self, word):
        """Получить слово, координаты и направление"""

        for elem in self.insertedList:
            if elem[0] == word:
                return elem

    def is_on_board(self, word):
        """Стоит ли слово уже на доске"""
        if self.word_info(word) is not None:
            return True
        else:
            return False

    def is_dir_okay(self, word, row, col, rev):
        """Стоит ли уже слово в том же направлении?
        """
        logging.debug("is dir okay for {} {} {} {}".format(
            word, row, col, rev))

        sameRev = []
        for elem in self.insertedList:
            if elem[3] == rev:
                sameRev.append(elem)

        logging.debug("sameRev filled")

        # Если на доске ещё ничего нет в том же направлении, всё в порядке
        if len(sameRev) == 0:
            logging.debug("sameRev is empty")
            return True

        # Пустить, только если слово стоит не раньше,
        # чем начинается другое
        if not rev:
            for elem in sameRev:
                # Если строка не совпадает, идти дальше
                if row != elem[1]:
                    logging.debug("row {} != {}".format(row, elem[1]))
                    continue
                if col > elem[2]:
                    if elem[2] + len(elem[0]) > col:
                        logging.debug("elem[2] + len > col")
                        return False
                else:
                    if col + len(word) > elem[2]:
                        logging.debug("col + len(w) > elem[2]")
                        return False
        else:
            for elem in sameRev:
                # Если столбец не совпадает, идти дальше
                if col != elem[2]:
                    logging.debug("col {} != {}".format(col, elem[2]))
                    continue
                if row > elem[1]:
                    if elem[1] + len(elem[0]) > row:
                        logging.debug("elem[1] + len(elem[0]) > row")
                        return False
                else:
                    if row + len(word) > elem[1]:
                        logging.debug("row + len(word) > elem[1]")
                        return False

        logging.info("dir okay for {}".format(word))
        return True

    def add_word_to_pos(self, word, row, col, rev=False):
        """Поставить слово на позицию. Изменяет сетку

        Parameters
        ----------
        word: Слово
        row: Ряд
        col: Столбец
        rev=False: По вертикали?
        """

        logging.debug("{} added to pos {} {} {}".format(word, row, col, rev))

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

        self.add_word_to_inserted(word, row, col, rev)

    def count_free_space(self, row, col, rev=False):
        """Сколько, начиная с данной клетки, места до границы или конца строки
        """
        logging.debug("count_free_space at {0} {1} {2}".format(row, col, rev))

        cell = self.cell

        if rev:
            grid = self.reverse(self.grid)
            row, col = col, row
        else:
            grid = self.grid

        i = col
        while i < len(grid):
            if rev:
                if cell(i, row) != "#":
                    i += 1
                else:
                    break
            else:
                if cell(row, i) != "#":
                    i += 1
                else:
                    break
            logging.debug("going through col #" + str(i))
        return i - col

    # def get_rulers(self):
    #     """Вернёт список направляющих
    #     в формате [направление, ряд, столбец]"""
    #     logging.debug("get rulers")

    #     res = []
    #     for si in range(len(self.canvas)):
    #         for sj in range(len(self.canvas)):
    #             if self.canvas[si][sj] in ["0", "1", "2"]:
    #                 res.append([self.canvas[si][sj], si, sj])
    #     return res

    def is_ruler_taken(self, row, col):
        """Взята ли направляющая?"""

        cell = self.canvas[row][col]

        if cell not in ["0", "1", "2"]:
            return True

        taken = 0
        for word in self.insertedList:
            if cell == "0":
                if word[1] == row and word[2] == col and word[3] is False:
                    return True
            elif cell == "1":
                if word[1] == row and word[2] == col and word[3] is True:
                    return True
            elif cell == "2":
                if word[1] == row and word[2] == col:
                    taken += 1
                if taken > 1:
                    return True

        return False

    def is_placeable(self, word, row, col, rev):
        """Можно ли разместить слово, начиная с этой позиции

        Выведет False, если слово помешает другому или встретит чёрную клетку
        Выведет True, если слово попадает в нужную букву
            или не пересекает слов вообще
        """
        logging.debug('is_placeable: {}'.format(word))

        firstCell = self.canvas[row][col]

        # Можно ли начать здесь слово по условию?
        if firstCell == "_" or firstCell == "#":
            logging.debug('firstCell == "_" or firstCell == "#"')
            return False

        if rev:
            # Можно ли поставить слово в таком направлении?
            if firstCell == "0":
                logging.debug('firstCell == "0"')
                return False

            grid = self.reverse(self.grid)
            row, col = col, row
        else:
            # Можно ли поставить слово в таком направлении?
            if firstCell == "1":
                logging.debug('firstCell == "1"')
                return False

            grid = self.grid

        # Не слишком ли слово длинное?
        if len(word) + col > len(grid):
            logging.debug('len(word) + col > len(grid)')
            return False

        # Нужной ли слово длины?
        if rev:
            if self.count_free_space(col, row, rev) != len(word):
                return False
        else:
            if self.count_free_space(row, col, rev) != len(word):
                return False

        # Вписывается ли слово?
        logging.debug("is_placeable loop")
        for i in range(col, col + len(word)):
            if grid[row][i] == "#":
                return False
            if grid[row][i] != word[i - col] and grid[row][i] != "_":
                if grid[row][i] in ['0', '1', '2']:
                    continue
                logging.debug("Not good at {} {} {}".format(row, i, rev))
                return False

        # Не стоит ли слово уже?
        if self.is_on_board(word):
            logging.debug("{} is already set".format(word))
            return False

        # Не будет ли слово включено в какое-то другое?
        if not self.is_dir_okay(word, row, col, rev):
            logging.debug("dir for {} is not okay".format(word))
            return False

        logging.info('{} is placeable at {}, {} {}'.format(
            word, row, col, rev))
        return True

    def put_word_on_desk(self, length):
        """Попробовать поставить слово на доску"""
        w = d.get_word(length, step=3)

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
                logging.debug("{} {}".format(i, j))

                if self.is_placeable(w, i, j, False):
                    self.add_word_to_pos(w, i, j, False)
                elif self.is_placeable(w, i, j, True):
                    self.add_word_to_pos(w, i, j, True)

    def creation(self, minLen=3, maxLen=11):
        trynumber = 0
        while True:
            trynumber += 1

            for i in reversed(range(minLen, maxLen)):
                self.put_word_on_desk(i)
            print("\n")
            grid.show()

            if trynumber > 300:
                trynumber = 0
                self.insertedList.pop()


grid = Grid(config.file_to_list(config.rgridFilePath), logging.INFO)

grid.creation()
