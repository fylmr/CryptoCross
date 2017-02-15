# -*- coding: utf-8 -*-

import codecs

with codecs.open('dict.txt', 'r', "utf_8_sig") as f:
    with codecs.open('list.txt', 'w', "utf_8_sig") as g:
        for x in f.readlines():
            x = x.rstrip()
            if not x:
                continue
            g.write(x.split(" ")[0])
            g.write("\n")
