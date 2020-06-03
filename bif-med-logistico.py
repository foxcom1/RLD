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

nome_bif = 'sim191107j-bif.dat'
nome_med = 'sim191107j-med.dat'
fbif = file(nome_bif, 'w')
fmed = file(nome_med, 'w')
x0 = 0.1
n = 100
tran = 10000

ri = 3.73
rf = 3.75
nr = 500
dr = (rf - ri)/nr
#ion()
ioff()
hold(True)
soma = 0.0
n_soma = 0
for r in arange(ri, rf, dr):
    x = logistico(x0, r, n, tran)
    plot([r]*len(x), x, ',r')
    for i in range(len(x)):
        fbif.write('%g %g\n' % (r, x[i]))
        fmed.write('%g %g\n' % (r, x.sum()/len(x)))


fbif.close()
fmed.close()
#plot(x, '.b')
show()
