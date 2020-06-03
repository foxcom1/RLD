#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

################################################################################################################################################################################################

# Esse programa pega uma sequencia de séries experimentais, cada série em um arquivo do tipo 'BaseNumero.dat' (exemplo: a seqüência 'exp031107c0.dat', 'exp031107c1.dat', ..., 'exp031107c299.dat') de apenas uma coluna, e transfere todos os pontos para um arquivo do tipo 'Base_bif.dat' (no exemplo acima: 'exp031107c-bif.dat'), de duas colunas, a primeira representando o parâmetro e a segunda a variável de cada arquivo.

################################################################################################################################################################################################

import os

base = raw_input('Digite o nome base (exemplo: os arquivos se chamam exp031107c0.dat, exp031107c1.dat, ..., exp031107c299.dat, portanto sua base é \'exp031107c\'): ')

N = int(raw_input('Quantidade de arquivos (como exemplo, para o caso anterior N = 300): '))

ini = float(raw_input('Início do intervalo de varredura do parâmetro de controle (por ex. 3.5): '))
fim = float(raw_input('Final do intervalo de varredura do parâmetro de controle (por ex. 5.5): '))

delta = (fim - ini) / N

nome_bif = base + '-bif.dat'
arq_bif = open(nome_bif, 'w')
nome_med = base + '-med.dat'
arq_med = open(nome_med, 'w')

for i in range(N):
	nome_arqi = base + str(i) + '.dat'
	arqi = open(nome_arqi, 'r')

	r = ini + i * delta

	N_soma = 0
	soma = 0.0
	for line in arqi:
		arq_bif.write('%g	%s\n' % (r, line.strip()))
		soma += float(line.strip())
		N_soma += 1

	if N_soma > 0 : arq_med.write('%.13f	%.13f\n' % (r, soma/N_soma))
	arqi.close()

arq_bif.close()
