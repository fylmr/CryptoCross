# -*- coding: utf-8 -*-
import config
import words
import logging

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

    def is_placeable(self, word, row, col, rev):
        """Можно ли разместить слово, начиная с этой позиции

        Выведет False, если слово помешает другому или встретит чёрную клетку
        Выведет True, если слово попадает в нужную букву
            или не пересекает слов вообще
        """

        cell = self.cell
        firstCell = cell(row, col)

        logging.debug('is_placeable: ' + word)

        # Можно ли начать здесь слово по условию?
        if firstCell == "_" or firstCell == "#":
            logging.debug('firstCell == "_" or firstCell == "#"')
            return False

        if rev:
            # Можно ли поставить слово в таком направлении?
            if firstCell == "0":
                logging.debug('firstCell == "0"')
                return False

            # grid = self.reverse(self.grid)
            row, col = col, row
        else:
            # Можно ли поставить слово в таком направлении?
            if firstCell == "1":
                logging.debug('firstCell == "1"')
                return False

            # grid = self.grid

        # # Не слишком ли слово длинное?
        # if len(word) + col > len(grid):
        #     logging.debug('len(word) + col > len(grid)')
        #     return False

        if self.count_free_space(row, col, rev) != len(word):
            return False

        logging.debug("is_placeable loop")
        for i in range(col, col + len(word)):
            if cell(row, i) == "#":
                return False
            if cell(row, i) != word[i - col] and cell(row, i) != "_":
                if cell(row, i) in ['0', '1', '2']:
                    continue
                return False

        logging.info('{} is placeable at {}, {} {}'.format(
            word, row, col, rev))
        return True


grid = Grid(config.file_to_list(config.rgridFilePath), logging.INFO)
grid.is_placeable("ПРИВЕТ", 6, 0, True)
