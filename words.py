import config
import random as rd
import time


class Words(object):
    """Работа со словами и словарём"""

    def __init__(self):
        super(Words, self).__init__()
        self.sortedList = config.file_to_list(config.sortedListPath)
        self.List = config.file_to_list(config.listPath)

    def get_word_len(self, length):
        """Find word of needed length

        Parameters
        ----------
        length
        binary -- take first word (faster)
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
