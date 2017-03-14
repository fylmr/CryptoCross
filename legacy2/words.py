# -*- coding: utf-8 -*-
import config
import random
import time


class Words(object):
    """Работа со словами и словарём"""

    def __init__(self):
        super(Words, self).__init__()
        self.wordList = config.file_to_list(config.sortedListFilePath)

    def get_word(self, length, step=1):
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

        n = random.randint(0, len(wordList) - 1)
        while len(wordList[n]) != length:
            if len(wordList[n]) > length:
                n += step
            else:
                n -= step
            if n < 0 or n > len(wordList):
                random.seed(round(time.time()))
                n = random.randint(0, len(wordList) - 1)

        return wordList[n]

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

    def letter_positions(self, word, letter, once=False):
        """Вернёт позиции, на которых данная буква находится в слове
        """
        res = []
        for letPos in range(len(word)):
            if word[letPos] == letter:
                res.append(letPos)
                if once:
                    return letPos

        return res
