#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

################################################################################################################################################################################################

# Esse programa faz um histograma do mapa logistico para cada valor de r.

################################################################################################################################################################################################

from pylab import *

#Funçao que calcula uma serie do mapa logistico para um dado parametro 'r' e condiçao inicial 'x0'.
#Um transiente de tamanho 'transiente' é descartado e 'n' pontos são guardados e retornados em um vetor 'x'.
def logistico(x0, r, n, transiente):
    xtmp = x0
    for i in range(transiente):
    	xtmp = r * xtmp * (1 - xtmp)
    x = zeros(n + 1, Float)
    x[0] = xtmp
    for i in range(n):
        x[i + 1] = r * x[i] * (1 - x[i])
    return x

#arquivo contendo a matriz com os pixels.
nom_arq_matriz = 'matriz.dat'
arq_matriz = file(nom_arq_matriz, 'w')


#condiçao inicial, tamanho do transiente e quantidade de pontos guardados para uma serie do mapa logistico.
x0 = 0.5
tran = 10000
n = 10000

#parametro inicial e final de varredura, com a quantidade de passos e o incremento.
ri = 2.9
rf = 3.7
nr = 10
dr = (rf - ri) / nr

#tamanho do vetor contendo os pixels verticais (para um valor de 'r') e seu incremento.
nx = 100
dx = 1.0 / nx

#matriz contendo todos os pixels. coluna representa o "histograma" de x para um dado 'r'.
matriz = zeros((nr, nx + 1), Float)

ion()
#ioff()
#hold(True)
hold(False)

for r in arange(ri, rf, dr):
    serie = logistico(x0, r, n, tran)

    #x é o vetor contendo os pixels verticais (histograma de x normalizado)
    hist = zeros(nx + 1, int)
    for ponto in serie:
        hist[int(round(nx * ponto, 0))] += 1

    #procedimento de normalização
    maximo = float(hist.max())
    #x = astype(Float) #prefiro nao arriscar o cast
    y = zeros(nx + 1, Float)
    for i in range(nx + 1):
        y[i] = hist[i] / maximo

    ind = int((r - ri) / dr)
    matriz[ind] = y

    t = arange(0, 1 + dx, dx)
    plot(t, y)

    nom_arq_hist = 'hist' + str(ind) + '.dat'
    arq_hist = file(nom_arq_hist, 'w')
    for i in range(nx + 1):
        arq_hist.write('%.10f %.10f\n' % (t[i], y[i]))

matriz = transpose(matriz)

for i in range(len(matriz)):
    for elemento in matriz[i]:
        arq_matriz.write('%g ' % elemento)
    arq_matriz.write('\n')

arq_matriz.close()

#plot(x, '.b')
#show()
