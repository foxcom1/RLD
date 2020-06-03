#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


from pylab import *

N = 1000
NL = 500
cut = 0.9*N
Li = 1.0
Lf = 20.0
dL = (Lf - Li)/NL



A = 0.85
B = -8.0
F = -2.7
Q = 2.0
K = -7.0


nome_arq = 'rld_perez_model_bif-2.dat'
arq = file(nome_arq, 'w')

for L in arange(Li, Lf, dL):
	x1 = -8.1
	for n in range(N):
		x2 = (A*x1 + F, A*K + F - L*((x1 - B)*(x1 - B) - (K - B)*(K - B)))[int(x1 < K)]
		x1 = x2
		if n > cut: arq.write('%g %g\n' % (L, x2))

arq.close()
