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


#nome_arq = 'sim191107j.dat'
#fp = file(nome_arq, 'w')
x0 = 0.1
n = 50 #quantidade de pontos para plotar
N = 100000 #quantidade de pontos para calcular medias
tran = 10000

rii = 2.9
rif = 3.737
rfi = 4.0
rff = 3.7385

nframes = 10
dri = (rif - rii) / nframes
drf = (rff - rfi) / nframes


nr = 100#quantidade de valores de parametros por figura

#ion()
ioff()
hold(True)
for ri, rf in zip(arange(rii, rif + dri, dri), arange(rfi, rff + drf, drf)):
	dr = (rf - ri) / nr
	for r in arange(ri, rf, dr):
		x = logistico(x0, r, N, tran)
		med = x.mean()
		x = x[:n]

		subplot(211)
		plot([r]*len(x), x, 'r,')
		
		subplot(212)
		plot([r], [med],'b.')
	arq_bif = 'logis' + str(int((ri - rii) / dri)) + '.jpg'
	savefig(arq_bif, dpi = 75)
	clf()
#    for i in range(len(x)):
        #fp.write('%g %g\n' % (r, x[i]))


#fp.close()

#plot(x, '.b')
#show()
