# -*- coding: utf-8 -*-
import logging
import os
import random
import time

import config
import words

# random.seed(42)


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
        """Получить клетку

        row, col: ряд, строка
        canvas: получить изначальную
        """
        if canvas:
            return self.canvas[row][col]
        else:
            return self.grid[row][col]

    def reverse(self, grid):
        """Транспонировать матрицу (сетку)"""

        gridRev = [[j[i] for j in grid] for i in range(len(grid))]
        for i in range(len(gridRev)):
            gridRev[i] = ''.join(gridRev[i])

        return gridRev

    def add_to_inserted(self, word, row, col, rev):
        """Добавить слово в insertedList"""
        self.insertedList.append([word, row, col, rev])

    def place(self, word, row, col, rev, force=False, noIns=False):
        """Поставить слово на позицию. Изменяет сетку

        word: Слово
        row: Ряд
        col: Столбец
        rev: По вертикали?
        force: Ставить, даже если слово уже есть
        noIns: Не добавлять в инсертед лист

        Returns:
        False, если слово уже в списке, а force не выставлен
        True, если всё ок

        """
        if not force:
            for listel in self.insertedList:
                if word == listel[0]:
                    return False

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

        if not noIns:
            self.add_to_inserted(word, row, col, rev)

        return True

    def clear(self):
        for i in range(len(self.grid)):
            self.grid[i] = self.canvas[i]

    def update(self):
        self.clear()
        for word in self.insertedList:
            self.place(word[0], word[1], word[2], word[3], True, True)

    def make_regex(self, row, col, rev):
        # logging.debug("making regex at {} {} {}".format(row, col, rev))

        regex = []
        regex += "\\b"

        if rev:
            grid = self.reverse(self.grid)
            row, col = col, row
        else:
            grid = self.grid

        i = col
        while i < len(grid):

            if grid[row][i] in ["_", "0", "1", "2"]:
                regex.append(".")
                # logging.debug("row {} col {}".format(row, i))
            elif grid[row][i] == "#":
                break
            else:
                regex.append(grid[row][i])

            i += 1

        regex += "\\b"

        # logging.debug("Regex made for {} {}".format(
        # [row, col, rev], ''.join(regex)))
        return ''.join(regex)

    def get_word_from_dict(self, row, col, rev, one=False):
        """
        Получить слово из словаря по заданному месту.
        Вызовет Warning, если слова не найдётся

        row
        col
        rev
        one

        Returns:
        Одно слово или список слов
        """
        regex = self.make_regex(row, col, rev)
        words = d.get_word_regex(regex, True)

        if len(words) < 1:
            raise Warning("В словаре нет нужных слов")

        if not one:
            return words

        i = random.randint(0, len(words) - 1)
        logging.debug(words[i])
        return words[i]

    def plusable(self, grid, row, col, brute=True):
        if row >= 0 and row < len(grid):
            if col >= 0 and col < len(grid):
                if brute:  # Проверить верх-низ или лево-право
                    if row - 1 < 0 or grid[row - 1][col] == "#":
                        if row + 1 == len(grid) or grid[row + 1][col] == "#":
                            return False
                    if col - 1 < 0 or grid[row][col - 1] == "#":
                        if col + 1 == len(grid) or grid[row][col + 1] == "#":
                            return False
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
                    if self.plusable(grid, plus[0] + i, plus[1] + j, False):
                        pluses.append([plus[0] + i, plus[1] + j])
            checked.append(plus)

        pluses = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == "+":
                    pluses.append([i, j])

        if get_pluses:
            return pluses
        return len(pluses)

    def get_fragment(self, row, col, get_length=False):
        """Получить направляющие, лежащие во фрагменте"""
        res = []
        for f in self.mark_fragment(row, col, True):
            if self.grid[f[0]][f[1]] in ['0', '1', '2']:
                r = f
                r.append(self.grid[f[0]][f[1]])
                res.append(r)

        if get_length:
            return len(res)
        return res

    def normalize_fragment(self, fragment):
        for i, ruler in enumerate(fragment):
            polarity = ruler[2]
            if polarity == '2':
                fragment[i] = [ruler[0], ruler[1], '0']
                fragment.append([ruler[0], ruler[1], '1'])
        return fragment

    def set_word(self, ruler):
        row = ruler[0]
        col = ruler[1]
        pol = ruler[2]

        if pol == '0':
            pol = False
        elif pol == '1':
            pol = True
        else:
            raise ValueError("Unexpected polarity")
            return False

        word = self.get_word_from_dict(row, col, pol, True)
        self.place(word, row, col, pol, force=False)

        return True


os.system('cls')

d = words.Words()
grid = Grid(config.file_to_list(config.gridPath), logging.DEBUG)

t0 = time.time()

# Создаём массив фрагментов
fragments = [grid.get_fragment(0, 1)]
#  grid.get_fragment(0, 8),
#  grid.get_fragment(8, 8)]
fragments = [grid.normalize_fragment(x) for x in fragments]
allrulers = fragments[0][:]  # + fragments[1] + fragments[2]
print(len(allrulers))
# checked = []

# Основной код

while True:
    i = random.randint(0, len(allrulers) - 1)
    ruler = allrulers[i]
    # Ставим слово
    try:
        # Если нашлось нужное слово, добавляем в инсертед лист
        grid.set_word(ruler)
        grid.show()
        allrulers.pop(i)
        logging.debug("Ruler {} removed, allrulers' len {}".format(
            ruler, len(allrulers)))
    except KeyboardInterrupt:
        print("PAUSE. PRESS ANY KEY TO CONTINUE OR CTRL+C TO EXIT.")
        input()
    except:
        # Если нет, удаляем из инсертед лист и копируем обратно в allrulers
        p = grid.insertedList.pop()
        if p[3] is True:
            allrulers.append([p[1], p[2], "1"])
        else:
            allrulers.append([p[1], p[2], "0"])
        grid.update()
        grid.show()
        logging.debug("Ruler {} appended".format(p))
    print("Lasted {0:.2f}s, {1} rulers left".format(-t0 +
                                                    time.time(), len(allrulers)))
    # Заканчиваем, когда all rulers обнулился
    if len(allrulers) < 1:
        break
    if len(allrulers) == 1:
        input()

print("\n-----------\n")
grid.show()
print(grid.insertedList)

print("Finished in {}".format(-t0 + time.time()))
