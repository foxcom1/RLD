#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pylab import *
### Parametros para se alterar:
#1. def F(x): o valor de r;
#2. d# -*- coding: iso-8859-1 -*-ef f(x): o mapa (F, F2, F3...) a ser plotado;
#3. x0: condição inicial;
#4. N: a quantidade de degraus da trajetoria no mapa;
#5. f_curva, f_reta e f_iterada: os nomes dos arquivos;
#6. if k > 50: o transiente a ser cortado;

#configurar plot interativo
ion()
hold(True)


#funcao a ser plotada
def F(x):
    return 3.5 * x * (1 - x)

def F2(x):
    return F(F(x))

def F3(x):
    return F(F(F(x)))

def F4(x):
    return F(F(F(F(x))))

def F5(x):
    return F(F(F(F(F(x)))))

def f(x):
    return F(x)


#inicializacao das variaveis
x0 = 0.2        #condicao inicial
lim = [x0, 0.0] #limites dos degraus
N = 10          #quantidade de degraus
kmin = 0

#plot da funcao e da reta diagonal
t = arange(0, 1, 0.0001)

subplot(121)
plot([0, 1], [0, 1], '-', t, f(t), 'r')
axis([0, 1, 0, 1])

for k in range(N):
    lim[1] = f(lim[0])

    if k > kmin:
	subplot(121)
        plot([lim[0]]*2, [lim[0], lim[1]], 'g', [lim[0], lim[1]], 2*[lim[1]], 'g')
	subplot(122)
	plot([k], [lim[1]], 'bo-')
	axis([kmin, N, 0, 1])
	arq_mapa = 'mapa' + str(k - 50) + '.jpg'
	savefig(arq_mapa, dpi = 75)

    lim[0] = lim[1]

