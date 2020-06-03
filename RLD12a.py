#!/usr/bin/env python
#-*- coding: iso-8859-15 -*-

############## Calcula séries para o circuito RLD utilizando o modelo de Jeffries e Buskirk
############## Salva o diagrama de bifurcação dos mínimos da tensão e máximos da corrente do diodo variando a freqüência do sinal de entrada
############## Calcula média da tensão e da corrente
############## Calcula média dos minimos de tensão e máximos de corrente
############## Modificado e adaptado para Python de programas de Hugo L. D. de S. Cavalcante e de Erika Medeiros
############## Por Fábio Oikawa dos Santos
############## 17/03/2006
############## Versão Beta


##### Módulos necessarios

#from math import *
from Numeric import *
import Gnuplot, os, time
#import strftime, localtime, time

##### Fim modulos necessarios
##### Inicializacao das variaveis globais

DIM = 3					#dimensao do sistema
d = 1.0e-7				#comprimento do passo de integracao
freq = 10.e3				#frequencia inicial de varredura
FF = 100.0e3				#frequencia final de varredura
N = 1000				#numero de passos na varredura de frequencia
PASSO = (FF-freq)/(N-1)			#comprimento do passo na varredura de frequencia
TAM = int(1e7) 			#tamanho da serie em uma certa frequencia
CUTser = int(TAM/2)				#corte na serie para diminuir o tamanho do arquivo
CUTbif = int(TAM/9)				#corte na série para eliminar o transiente no diagrama de bifurcação
CUTmed = int(TAM/10)
#itermin = 100000			#?
#cutb = 9l*itermin/10l			#?
#cutm = 1l*(itermin/5l)			#?
#MAXMAX = 500				#maximos para o diagrama de bifurcação
#Vc = 3e-3				#que e isso?
#dVc = 0.3

Cs0 = 6.0e-13				#veja formulas abaixo definidas
Cj0 = 6.0e-10
phi = 0.04
Phi = 0.6
I0 = 4.8e-9

L = 1.0e-2
R = 100.
V0s = 2.5				#amplitude da senoide de entrada

Vi = 0. 				#tensão inicial no diodo
Ii = 0.					#corrente inicial no diodo
thetai = 0.				#fase inicial no sinal de entrada (omega*t)

###### Fim inicializacao das variaveis globais
#### Definicao das funcoes

def Cj(V):
  return Cj0/sqrt(1-V/Phi)

def Cs(V):
  return Cs0*exp(V/phi)

def Id(V):				#corrente no diodo
  return I0*(exp(V/phi)-1)

def C(V):				#capacitancia total na juncao
  return Cj(V)+Cs(V)

def V0(theta):				#sinal de entrada
  return V0s*sin(theta)

def f(V, I, theta):			#dV/dt
  return (I-Id(V))/C(V)

def g(V, I, theta):			#dI/dt
  return (V0(theta)-R*I-V)/L

def h(V, I, theta):			#d(theta)/dt
  return omega

F = [f, g, h]				#lista das funcoes

##### Função que lê diretório e cria subdiretório (localtime) para guardar os arquivos
def Cria_dir():
  HOME = os.environ['HOME']		#diretorio home do usuario
  HOME1 = '/home1/oikawa/DADOS'
  SUBDIR = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())	#cria um subdiretório tendo data e hora como nome
  while True:
    diretorio = raw_input(' Diretório existente e com permissão de escrita para os arquivos (enter para %s): ' % HOME1)
    if (diretorio == ''): diretorio = HOME1; break				#caso 'enter'
    if (os.path.isdir(diretorio))and(os.access(diret,7)): break		#controle de acesso ao diretório
  subdir = raw_input(' Subdiretório para esta aquisição (enter para "%s"): %s/' % (SUBDIR, diretorio))
  if (subdir == ''): subdir = '/'+SUBDIR
  os.mkdir(diretorio+subdir)
  return diretorio+subdir

##### Função que abre arquivo num dado diretorio
def Cria_arq(diretorio, nome_arq, texto):
  nome = raw_input(texto + diretorio + '/')
  if (nome == ''): nome = nome_arq
  return open(diretorio + '/' + nome,'w')

##### Método de Runge-Kutta para resolução de eq. diferenciais (não utilizei no algoritmo principal)
def rk4o(k = zeros((5,DIM), Float), x = array([0.,0.,0.]), F = [f, g, h]): #função que resolve EDO por Runge Kutta 4a ordem
  for i in range(1,4):	#calculo de k1, k2 e k3
    for j in range(DIM):
      k[i][j] = d*F[j](x[4][0]+0.5*k[i-1][0],x[4][1]+0.5*k[i-1][1],x[4][2]+0.5*k[i-1][2])
  for j in range(DIM):	#calculo de k4
    k[4][j] = d*F[j](x[4][0]+k[3][0],x[4][1]+k[3][1],x[4][2]+k[3][2])
  for j in range(DIM):	#calculo de x (V, I e theta)
    dx[j] = (k[1][j]+2.0*k[2][j]+2.0*k[3][j]+k[4][j])/6.
    x[0][j], x[1][j], x[2][j], x[3][j] = x[1][j], x[2][j], x[3][j], x[4][j] #x[0]=x(4. anterior), x[1]=x(3. anterior), x[2]=x(2. anterior), x[3]=x(anterior), x[4]=x(presente)
    x[4][j] += dx[j]	#x(presente)
  return k, x

  
  
  
##### Abertura dos arquivos para dados

diret = Cria_dir()
med = Cria_arq(diret, 'med.dat', ' Arquivo para as médias temporais (enter para "med.dat"): ')
medmax = Cria_arq(diret, 'medmax.dat', ' Arquivo para as médias dos máximos (enter para "medmax.dat"): ')
bifV = Cria_arq(diret, 'bifV.dat', ' Arquivo para o diagrama de bifurcação (tensao) (enter para "bifV.dat"): ')
bifI = Cria_arq(diret, 'bifI.dat', ' Arquivo para o diagrama de bifurcação (corrente) (enter para "bifI.dat"): ')
bif = [bifV, bifI]

nomeserie = raw_input(' Arquivo (não ponha o ".dat") para a série temporal (enter para "serie[i].dat"): %s/' % diret)
if (nomeserie == ''): nomeserie = 'serie'

info = open(diret+'/info.txt','w')	#arquivo para guardar informações sobre a aquisição
info.write('# Comprimento do passo de integracao (d): %f\n' % d)
info.write('# Numero de passos na varredura de frequencia (N): %d\n ' % N)
info.write('# Tamanho da serie em uma certa frequencia (TAM): %d\n ' % TAM)
info.write('# Corte na serie para diminuir o tamanho do arquivo (CUTser): %d\n ' % CUTser)
info.write('# Corte na serie para evitar o transiente na bifurcação (CUTbif): %d\n ' % CUTbif)
info.write('# Corte na serie para evitar o transiente na média (CUTmed): %d\n ' % CUTmed)
info.write('# R=%f\tL=%f\tV0s=%f\n' % (R, L, V0s))
info.write('# frequencia inicial=%f\n# frequencia final=%f\n' % (freq, FF))
info.write('# Phi=%f\tphi=%f\n' % (Phi, phi))
info.write('# Cs0=%f\tCj0=%f\tI0=%f\n' % (Cs0, Cj0, I0))
info.write('# Vi=%f\tIi=%f\tthetai=%f\n' % (Vi, Ii, thetai))
info.close()

for i in range(2):
  bif[i].write('# frequencia inicial=%.13f\n# frequencia final=%.13f\n' % (freq, FF))
  bif[i].write('# R=%.13f\tL=%.13f\tV0s=%f\n' % (R, L, V0s))
  bif[i].write('# Phi=%.13f\tphi=%.13f\n' % (Phi, phi))

medmax.write('# frequencia inicial=%.13f\n# frequencia final=%.13f\n' % (freq, FF))
medmax.write('# R=%.13f\tL=%.13f\tV0s=%f\n' % (R, L, V0s))
medmax.write('# Phi=%.13f\tphi=%.13f\n' % (Phi, phi))

med.write('# frequencia inicial=%.13f\n# frequencia final=%.13f\n' % (freq, FF))
med.write('# R=%.13f\tL=%.13f\tV0s=%f\n' % (R, L, V0s))
med.write('# Phi=%.13f\tphi=%.13f\n' % (Phi, phi))

print(' Calculando...')

####### Fim abertura dos arquivos para dados
### Varredura em frequencia

#T0 = time()				#tempo inicial de execucao do programa

for n in range(N):			#n varia a frequencia
	serie = open(diret+'/'+nomeserie + str(n+1) + '.dat','w')
	serie.write('# Tensão: %f\tFrequencia: %f' % (V0s, freq))
	soma = somamax = array([0.,0.])
	nmax = array([0, 0])
	x = zeros((5,3), Float)
	dx = array([0., 0., 0.])
	k = zeros((5,DIM), Float)
	t = 0.
	omega = 2*pi*freq
	start = False
	
##### Laco calcula a serie
	
	for cont in range(TAM):
	  t += d
##### Runge Kutta de ordem 4

	  k, x = rk4o(k, x, F)

##### Fim Runge Kutta de ordem 4
##### Guardar serie e maximos

   	  if (cont > CUTser):		#guarda parte da série temporal
	    serie.write('%.13f\t%.13f\t%.13f\n' % (t, x[4][0], x[4][1]))
	  if (not(start))and(cont > CUTmed):	#início da soma para a média temporal
	    start = True
	    contini = cont
	  if (start):
	    soma[0] += x[4][0] #soma de V
	    soma[1] += x[4][1] #soma de I
	  if (cont > CUTbif)and(x[2][0] < x[0][0])and(x[2][0] < x[1][0])and(x[2][0] < x[3][0])and(x[2][0] < x[4][0]):   #minimos tensão V (Va>V e Va>Vaa)
	    somamax[0] += x[2][0]
	    nmax[0] += 1
	    bif[0].write('%.13f %.13f\n' % (freq, x[2][0]))
#	  if (x[1][1] >= x[2][1])and(x[1][1] <= x[0][1]):   #maximos corrente (Ia>I e Ia>Iaa)
#	    somamax[1] += x[1][1]
#	    nmax[1] += 1
#	    bif[1].write('%.13f %.13f\n' % (freq, x[1][1]))

##### Fim guardar serie e maximos
##### Fim laco calcula a serie
##### Media das variaveis
	print('f: %.13f medV: %.13f medI: %.13f' % (freq, soma[0]/(cont-contini), soma[1]/(cont-contini)))
	med.write('%.13f %.13f %.13f\n' % (freq, soma[0]/(cont-contini), soma[1]/(cont-contini)))
	if (nmax[0] != 0.)and(nmax[1] != 0.):
	  medmax.write('%.13f %.13f %.13f\n' % (freq, somamax[0]/nmax[0], somamax[1]/nmax[1]))
	freq += PASSO
	serie.close()

##### Fim media das variaveis
##### Fum varredura em frequencia

med.close()
medmax.close()
bif[0].close()
bif[1].close()
print(' Cálculo completo.')
    
    
    
    
    
    
    

#x1=array([Vi,Ii,thetai])
#calc(x1)
#print('\nTempo de calculo: ' + str(time()-T0))

#g=Gnuplot.Gnuplot()
#g('set ylabel \'V\'\n')
#g("set xlabel \"theta\"\n")
#g("plot \"%s.dat\" using 2:3:4 title 'Circuito RLD'\n" % file)
#g("pause 3\n")
#g("set multiplot\n")
#g("set size 0.5, 1\n")
#g("set origin 0,0\n")
#g("set xlabel \"t\" \n")
#g("set ylabel \"\"\n")
#g("plot \"rld.dat\" using 1:2 t \"V\", \"\" u 1:3 t \"I\" \n")
#g("set origin 0.5,0\n")
#g("set title \"Circuito RLD\"\n")
#g("set xlabel \"V\" \n")
#g("set ylabel \"I\"\n")
#g("plot \"rld.dat\" using 2:3 t \"\"\n")
#g("set nomultiplot\n")
#g("pause -1\n")
