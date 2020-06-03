#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

################################################################################################################################################################################################

# Esse programa calcula a média do diagrama de bifurcação contido em um arquivo de duas colunas (r, x) e salva em outro arquivo de mesmo nome-base, porém com terminação '-med.dat'.

################################################################################################################################################################################################

import os

base = raw_input('Digite o nome base (exemplo: o arquivo se chama \'exp031107c-bif.dat\', logo sua base é \'exp031107c\'): ')

nome_med = base + '-med.dat'
arq_med = open(nome_med, 'w')

nome_bif = base + '-bif.dat'
arq_bif = open(nome_bif, 'r')

for line in arq_bif:
	

arq_med.close()
arq_bif.close()
