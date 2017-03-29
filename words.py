import config
import random as rd
import time
import re


class Words(object):
    """Работа со словами и словарём"""

    def __init__(self):
        super(Words, self).__init__()
        self.sortedList = config.file_to_list(config.sortedListPath)
        self.alphaList = config.file_to_list(config.listPath)

    def get_word_len(self, length):
        """Find word of needed length

        Parameters
        ----------
        length

        Returns
        -------
        word
        """

        sortedList = self.sortedList

        step = rd.randint(0, length) * round(time.time())
        print(step)

        n = rd.randint(0, len(sortedList) - 1)
        print(n)
        while len(sortedList[n]) != length:
            if len(sortedList[n]) > length:
                n += step
            else:
                n -= step
            if n < 0 or n > len(sortedList):
                n = rd.randint(0, len(sortedList) - 1)

        return sortedList[n]

    def get_word_regex(self, regex, many=False):
        """Получить слово или несколько слов, которые
        удовлетворяют регекспу"""

        if many:
            words = []
        for word in self.alphaList:
            if re.match(regex, word):
                if not many:
                    return word
                words.append(word)
        if many:
            return words
