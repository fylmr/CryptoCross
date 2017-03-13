# -*- coding: utf-8 -*-

import codecs
import random

res = []

with codecs.open('listsorted.txt', 'r', "utf_8_sig") as f:
    res = f.readlines()

res = list(res)
random.shuffle(res)
res = [x.strip() for x in res]
res = sorted(res, key=len)
res.reverse()

with codecs.open('listsorted.txt', 'w', "utf_8_sig") as g:
    for item in res:
        g.write("%s\n" % item)
