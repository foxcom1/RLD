#!/usr/bin/env python

#from pylab import *
import os

nome_orig = raw_input("\nNome do arquivo: ")
if nome_orig[-4:]=='.dat':
	for j in range(5,7):
		nome_dest = nome_orig[:-4] + '-mapa' + str(j) + '.dat'
		
		orig = open(nome_orig, 'r')
		dest = open(nome_dest, 'w')
		lista = []
		for line in orig:
			lista.append(line.strip())

		mapa = [(lista[i], lista[i + j]) for i in range(len(lista) - j)]

		for i in range(len(mapa)):
			dest.write(mapa[i][0] + ' ' + mapa[i][1] + '\n')

		orig.close()
		dest.close()
