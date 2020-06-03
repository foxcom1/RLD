#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#from pylab import plot, show
from pylab import *
import time

def logistico(x0, r, n, transiente):
    xtmp = x0
    for i in range(transiente):
    	xtmp = r * xtmp * (1 - xtmp)
    x = zeros(n + 1, Float)
    x[0] = xtmp
    for i in range(n):
        x[i + 1] = r * x[i] * (1 - x[i])

    return x


x0 = 0.1000
r = 3.6
n = 70
tran = 0

x = logistico(x0, r, n, tran)

ioff()
hold(False)
f = file('serie-logistico-4.dat', 'w')
for i in range(len(x)):
    f.write('%g\n' % x[i])
f.close()
plot(x, 'b')
plot(x, '.b')
show()
