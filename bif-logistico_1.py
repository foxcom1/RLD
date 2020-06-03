#!/usr/bin/env python
# -*- coding: cp860 -*-

# programa que calcula e plot o mapa de henon. patra usar a função henon (e não a henon2) utilize a primeira linha de importação (apenas plot e show). Por Fabio Oikawa

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

nome_arq = 'sim191107j.dat'
fp = file(nome_arq, 'w')
x0 = 0.1
n = 100
tran = 10000

ri = 2.9
rf = 4.0
nr = 500
dr = (rf - ri)/nr
#ion()
ioff()
hold(True)
for r in arange(ri, rf, dr):
    x = logistico(x0, r, n, tran)
    plot([r]*len(x), x, ',r')
    for i in range(len(x)):
        fp.write('%g %g\n' % (r, x[i]))


fp.close()

#plot(x, '.b')
show()
