# -*- coding: utf-8 -*-
import config
import words
import logging

class Grid(object):
    """Работа с сеткой кроссворда"""
    def __init__(self, arg):
        super(Grid, self).__init__()
        self.arg = arg
        