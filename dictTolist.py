# -*- coding: utf-8 -*-
i = 0
with open('dict.txt', 'r') as f:
    with open('list.txt', 'w') as g:
        for x in f.readlines():
            x = x.rstrip()
            if not x:
                continue
            g.write(x.split(" ")[0])
            g.write("\n")
