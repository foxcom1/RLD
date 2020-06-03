#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from pylab import *
### Parametros para se alterar:
#1. def F(x): o valor de r;
#2. def f(x): o mapa (F, F2, F3...) a ser plotado;
#3. x0: condição inicial;
#4. N: a quantidade de degraus da trajetoria no mapa;
#5. f_curva, f_reta e f_iterada: os nomes dos arquivos;
#6. if k > 50: o transiente a ser cortado;

#configurar plot interativo
ion()
hold(True)


#funcao a ser plotada
def F(x):
    return r * x * (1 - x)

def F2(x):
    return F(F(x))

def F3(x):
    return F(F(F(x)))

def F4(x):
    return F(F(F(F(x))))

def F5(x):
    return F(F(F(F(F(x)))))

def f(x):
    return F5(x)

#def salvar_curva(x, y):
     #for i in range(len(x)):
        #f_curva.write('%g %g\n' % (x[i], y[i]))

#def salvar_reta(x, y):
     #for i in range(len(x)):
        #f_reta.write('%g %g\n' % (x[i], y[i]))

#def salvar_iterada(x, y):
     #for i in range(len(x)):
        #f_iterada.write('%g %g\n' % (x[i], y[i]))

#inicializacao das variaveis
#x0 = 0.5        #condicao inicial
#lim = [x0, 0.0] #limites dos degraus
#N = 10          #quantidade de degraus
#f_curva = file('sim191107h-curva.dat', 'w')
#f_reta = file('sim191107h-reta.dat', 'w')
#f_iterada = file('sim191107h-iter.dat', 'w')

#plot da funcao e da reta diagonal
t = arange(0, 1, 0.0001)
#salvar_curva(t, f(t))
#salvar_reta([0,1], [0,1])
ri = 3.7365
rf = 3.7382
nr = 51
dr = (rf - ri) / nr

for r in arange(ri, rf, dr):
    a = axes([0, 0, 1, 1])
    plot([0, 1], [0, 1], t, f(t), 'r')

    a = axes([.3, .15, .3, .3], axisbg = 'w')
    setp(a, xticks=[], yticks=[])

    x0 = 0.5        #condicao inicial
    lim = [x0, 0.0] #limites dos degraus
    N = int(2 + 0.01 * ((r - ri) / dr) * ((r - ri) / dr))

    plot([0, 1], [0, 1], t, f(t), 'r')
    for k in range(N):
        lim[1] = f(lim[0])
        plot([lim[0]]*2, [lim[0], lim[1]], 'g', [lim[0], lim[1]], 2*[lim[1]], 'g')
        axis([0.5, 0.52, 0.5, 0.52])
        lim[0] = lim[1]

    arq_mapa = 'inter' + str(int((r - ri) / dr)) + '.jpg'
    savefig(arq_mapa, dpi = 75)
    clf()

#for k in range(N):
    #lim[1] = f(lim[0])

    #if k > 50:
        ##salvar_iterada([lim[0]]*2, [lim[0], lim[1]])
        #plot([lim[0]]*2, [lim[0], lim[1]], 'g')
        ##salvar_iterada([lim[0], lim[1]], 2*[lim[1]])
        #plot([lim[0], lim[1]], 2*[lim[1]], 'g')

    #lim[0] = lim[1]

#f_curva.close()
#f_iterada.close()
#f_reta.close()
#show()
