/* O programa calcula uma serie temporal da tensao no diodo (RLD) e grava num arquivo
Calculado por metodo de Runge-Kutta de quarta ordem        */

// o diodo esta "dirigido" para o terra, entao peguei a tensao no diodo com sinal trocado para ficar "para cima".

# include <stdlib.h>
# include <stdio.h>
# include <math.h>
# include <time.h>
# include <string.h>

# define dim 3

/*
Equacoes para Oscilador Nao-linear usando Diodo
dV/dt = (I-Id)/C
dI/dt = [V0 sen(omega t) - RI - V]/L
dteta/dt = omega
Id = Is[exp(V/nVt) - 1]
C = Cj + Cd
Cj = Cj0(1 - V/V0)^m, 1/3 <= m <= 1/2
Cd = (Tt/Vt) I = Cd0 exp(V/nVt)
*/
/*
Modelo da ON semicontuctor para spice3.

**************************************
*      Model Generated by MODPEX     *
*Copyright(c) Symmetry Design Systems*
*         All Rights Reserved        *
*    UNPUBLISHED LICENSED SOFTWARE   *
*   Contains Proprietary Information *
*      Which is The Property of      *
*     SYMMETRY OR ITS LICENSORS      *
*Commercial Use or Resale Restricted *
*   by Symmetry License Agreement    *
**************************************
* Model generated on May 30, 03
* MODEL FORMAT: SPICE3
.MODEL 1n4007 d
+IS=7.02767e-09 RS=0.0341512 N=1.80803 EG=1.05743
+XTI=5 BV=1000 IBV=5e-08 CJO=1e-11
+VJ=0.7 M=0.5 FC=0.5 TT=1e-07
+KF=0 AF=1

Fairchild
.MODEL  1N4007  D
+ IS = 3.872E-09
+ RS = 1.66E-02
+ N = 1.776
+ XTI = 3.0
+ EG = 1.110 
+ CJO = 1.519E-11
+ M = 0.3554
+ VJ = 0.5928
+ FC = 0.5
+ ISR = 1.356E-09
+ NR = 2.152
+ BV = 1000.0
+ IBV = 1.0E-03

   nk/e = 0.0001530440149438464198 V/K
   T = 300 K ==> nkT/e = phi = 0.04591320448315392593 V
   Cs0 = (TT)x(IS)x(q/nkT) = Cd0 = 8.433303759968834153e-15
*/


/******* par�metros de entrada dos arquivos especificados em input ***********/ 
double	/* par�metros do gerador */
	Vg,		//amplitude de entrada.
	f,		//freq��ncia de entrada.
	dc,		//offset de entrada.
	inicial,	//valor inicial do par�metro de controle.
	final;		//valor final do par�metro de controle.
char	var[5];		//vari�vel de controle (freq��ncia, amplitude ou offset).

	/* par�metros de varredura */ 
double	d;		//dt (passo de integra��o).
long	itermin,	//n�mero minimo de itera��es.
	itermax,	//n�mero m�ximo de itera��es.
	peakmax,	//n�mero m�ximo de picos adquiridos para o diagrama.
	n_step;		//quantidade de steps.

	/* par�metros do diodo */
double	Cd0,		//capacit�ncia de difus�o para V(diodo) ~ 0.
	Tt,		//tempo m�dio de tr�nsito.
	Cj0,		//capacit�ncia de deple��o (capacit�ncia de jun��o) para V(diodo) ~ 0.
	n,		//coeficiente de emiss�o (n ~ 2). vide wikipedia.
	Vt,		//tens�o t�rmica (kT/e ~ 26mV). vide wikipedia.
	V0,		//tens�o interna
	Is,		//corrente de satura��o

	/* par�metros do circuito */
	R,		//resist�ncia.
	L,		//indut�ncia.
	Vi,		//tens�o inicial no diodo.
	Ii,		//corrente inicia na malha.
	thetai;		//(wt) - fase inicial.

char	nomebif[256],	//nome para o arquivo do diagrama de bifurca��o.

/******* fim dos par�metros de entrada dos arquivos especificados em input ***********/ 


double	omega = 6.2831853071795862 * f;

char	nome_arq_param[256];

void getname(char name[256]) {
	printf(" Entre com o nome do arquivo a ser gravado: ");
	scanf("%s", name);
	printf("\n");
}

/* equacoes auxiliares */
double Id(double Isinter, double Vinter, double nVtinter) {
	return Isinter * (exp(Vinter/nVtinter) - 1);
}

double Cd(double Cd0int, double Vint, double nVtint) {
	return Cd0int * exp(Vint/nVtint);
}

double Cj(double Cj0int, double Vint, double V0int) {
	return Cj0int/sqrt(1.0 - Vint/V0int);
}

double C(double Cd0int, double Cj0int, double Vint, double nVtint, double V0int) {
	return Cd(Cd0int, Vint, nVtint)+Cj(Cj0int, Vint, V0int);
}

/* funcoes das equacoes diferenciais  */

double fI(double Iint, double Vint, double thetaint) {
	return (Vg * sin(thetaint) - R*Iint - Vint)/L;
}

double fV(double Iint, double Vint, double thetaint) {
	return (Iint - Id(Is, Vint, nVt)) / C(Cd0, Cj0, Vint, nVt, V0);
}

double ftheta() {
	return omega;
}


double rk4(double x) {

	long	cont,
		nummax;

	double	k1[dim],
		k2[dim],
		k3[dim],
		k4[dim];

	double	I = Ii,
		V = Vi,
		theta = thetai,
		xa = 0.0,
		xaa,
		step,
		t;

	printf(" Iniciando o calculo \r\n");

	step = (final - inicial) / (n__step - 1);
	fprintf(bif,"# %s inicial=%.13lf\n# final=%.13lf\n", var, inicial, final);
	for (x = inicial; x < final; x += step) {
		t = 0.0;
		V = Vi;
		I = Ii;
		nummax = 0;
		for (cont=0l; cont <= itermax; cont++) {
			/* as linhas abaixo constituem o algoritmo de Runge-Kutta de quarta ordem */
			k1[0] = d*fI(I, V, theta);
			k1[1] = d*fV(I, V, theta);
			k1[2] = d*ftheta(I, V, theta);

			k2[0] = d*fI(I+k1[0]/2.0, V+k1[1]/2.0, theta+k1[2]/2.0);
			k2[1] = d*fV(I+k1[0]/2.0, V+k1[1]/2.0, theta+k1[2]/2.0);
			k2[2] = d*ftheta(I+k1[0]/2.0, V+k1[1]/2.0, theta+k1[2]/2.0);
			
			k3[0] = d*fI(I+k2[0]/2.0, V+k2[1]/2.0, theta+k2[2]/2.0 );
			k3[1] = d*fV(I+k2[0]/2.0, V+k2[1]/2.0, theta+k2[2]/2.0 );
			k3[2] = d*ftheta(I+k2[0]/2.0, V+k2[1]/2.0, theta+k2[2]/2.0 );

			
			k4[0] = d*fI(I+k3[0], V+k3[1], theta+k3[2]);
			k4[1] = d*fV(I+k3[0], V+k3[1], theta+k3[2]);
			k4[2] = d*ftheta(I+k3[0], V+k3[1], theta+k3[2]);

			Iaa = Ia;
			Ia = I;

			I += (k1[0]+2.0*k2[0]+2.0*k3[0]+k4[0])/6.0;
			V += (k1[1]+2.0*k2[1]+2.0*k3[1]+k4[1])/6.0;
			theta += (k1[2]+2.0*k2[2]+2.0*k3[2]+k4[2])/6.0;

			t += d;

			/* corta o transiente e localiza um maximo  da corrente */
			if ((cont>cutb) && (Ia>I) && (Ia>Iaa) && (nummax<peakmax)) {
				  fprintf(bif, "%.13lf %.13lf\n", x, R*Ia); 
				  nummax++;
			} //end if

			if (nummax>peakmax) {
				break;
			} //end if
		}//end for
		printf("\n Vg = %.13lf", V0);
		fflush(bif);
	}//end for
	fclose(bif);

	printf("\n Calculo completo em segundos.\n");
	printf("Arquivo: %s\n", nomebif);
}

int main (void) {

	FILE	*bif,//arquivo com os pontos para o diagrama de bifurca��o
		*input,//entrada contendo todos os nomes dos arquivos com par�metros
		*arq_param;//arquivo com os par�metros

	char	parametros[80],//par�metros extra�dos do arquivo *arqparam
		nome_arq_param[10]

	time_t	tempo0,
		tempo1;

	/* output to screen */
	printf("PROGRAM RLDA.\n" ) ;
	printf("(Version C 1.0 - 200 - by FOdS )\n" ) ;

	if ((input = fopen("input.dat","r")) == NULL) {
		printf("O arquivo n�o pode ser aberto\n");
		exit(1);
	}

	while(!feof(input)) {


		const double cutb = 9l*itermin/10l;

		fscanf(input, "%s", nome_arq_param);
//		q = strlen(nomearqdados);
//		nomearqdados[q - 3] = 'd';
//		nomearqdados[q - 2] = 'a';
//		nomearqdados[q - 1] = 't';
		if ((arq_param = fopen(nome_arq_param, "r")) == NULL) {
			printf("O arquivo n�o pode ser aberto\n");
			break;
		}

		/* parameters initialization from file */	
		fscanf(arq_param, "%lf %lf %s %lf %lf %d", &V0, &freq, var, &inicial, &final, &n_iter);
		fscanf(arq_param, "%lf %d %d %d", &d, &itermin, &itermax, &MAXMAX);
		fscanf(arq_param, "%lf %lf %lf %lf %lf", &Cs0, &Cj0, &phi, &Phi, &I0);
		fscanf(arq_param, "%lf %lf", &L, &R);
		fscanf(arq_param, "%lf %lf %lf", &Vi, &Ii, &thetai);



		fclose(arq_param);

		printf("%f %f %f %f %f\n",  ) ;



	}
	
	fclose(arquivo);	 
	printf("All files calculated. \n");
	return 0;
}
/*   da main  */   
//----------------------------------End Main---------------------------------





		//double somaV, somaI, dVa=0.0, dV=0.0;  
	
		printf("\r\n");
	//	printf("\tUsando frequencia como parametro de controle\n");
		printf("\tEquacoes para Oscilador Nao-linear usando Diodo \n\n");
		printf("\t\t dV/dt = (I-Id)/C\n");
		printf("\t\t dI/dt = [V0 sen(omega t) - RI - V]/L  \n");
		printf("\t\t dteta/dt = omega \n");
		printf("\t\t Id = I0[exp(V/phi)-1]\n");
		printf("\t\t C = Cj+Cs\n");
		printf("\t\t Cj = Cj0(1-V/Phi)^(-1/2)\n");
		printf("\t\t Cs = Cs0exp(V/phi)\n\n");
		printf("\n");




	//	printf(" Para a serie:\n");
	//	getname(nomeserie);
	//	serie = fopen(nomeserie, "wt");
		printf(" Para o diagrama de bifurca��o,\n");
		getname(nomebif);
		bif = fopen(nomebif,"wt");
	
	//	printf(" Para as m�dias,\n");
	//	getname(nomemed);
	//	med = fopen(nomemed,"wt");
	
		printf(" Iniciando o calculo \r\n");
		tempo0 = time(NULL);
	
		//	for (j=0;j<3;I[j++]=Ii); U=Ui; W=Wi; Ub=Ubi; 
		//step=(omegafinal-omegainicial)/num;
		step = (V0final - V0inicial) / (num - 1);
	//	Va=0.0; I=0.0;
		fprintf(bif,"# V0ini=%.13lf\n# V0final=%.13lf\n", V0inicial, V0final);
	//	fprintf(med,"# V0ini=%.13lf\n# V0final=%.13lf\n",
	//		V0inicial, V0final);
		for (V0 = V0inicial; V0 < V0final; V0 += step) {
	//		somaV = 0.0;
	//		somaI = 0.0;
			t = 0.0;
			V = Vi;
			I = Ii;
			nummax = 0;
	//		start=0; stop=0; nummax=0;
			for (cont=0l; cont <= itermax; cont++) {
				/* as linhas abaixo constituem o algoritmo de Runge-Kutta de quarta ordem */
				k1[0] = d*fI(I, V, theta);
				k1[1] = d*fV(I, V, theta);
				k1[2] = d*ftheta(I, V, theta);
	
				k2[0] = d*fI(I+k1[0]/2.0, V+k1[1]/2.0, theta+k1[2]/2.0);
				k2[1] = d*fV(I+k1[0]/2.0, V+k1[1]/2.0, theta+k1[2]/2.0);
				k2[2] = d*ftheta(I+k1[0]/2.0, V+k1[1]/2.0, theta+k1[2]/2.0);
				
				k3[0] = d*fI(I+k2[0]/2.0, V+k2[1]/2.0, theta+k2[2]/2.0 );
				k3[1] = d*fV(I+k2[0]/2.0, V+k2[1]/2.0, theta+k2[2]/2.0 );
				k3[2] = d*ftheta(I+k2[0]/2.0, V+k2[1]/2.0, theta+k2[2]/2.0 );
	
				
				k4[0] = d*fI(I+k3[0], V+k3[1], theta+k3[2]);
				k4[1] = d*fV(I+k3[0], V+k3[1], theta+k3[2]);
				k4[2] = d*ftheta(I+k3[0], V+k3[1], theta+k3[2]);
	
	//			dVa = dV;
	//			dV = (k1[1]+2.0*k2[1]+2.0*k3[1]+k4[1])/6.0;
	
				Iaa = Ia;
				Ia = I;
	
				I += (k1[0]+2.0*k2[0]+2.0*k3[0]+k4[0])/6.0;
				V += (k1[1]+2.0*k2[1]+2.0*k3[1]+k4[1])/6.0;
				theta += (k1[2]+2.0*k2[2]+2.0*k3[2]+k4[2])/6.0;
	
	//			fprintf(serie, "%.13lf %.13lf\n", t, R*I); 
		
				t += d;
	//			printf("\n V0 = %f ## t = %f ## I = %f ## V = %f", V0, t, I, V);
	
		
	//			Vaa = Va;
	//			Va = V;
	//			}
	//			if ((start==0)&&(cont>cutm)&&(I>Ic)&&(fabs(dI)<dIc))
	//				{
	//				start=1;
	//				contini=cont;
	//				}
	//			if (start) 
	//			  {
	//			    somaV+=V;
	//			    somaI+=I;
	//			  }
	
				if ( (cont>cutb)&&(Ia>I)&&(Ia>Iaa)&&(nummax<MAXMAX) ) {
		/* corta o transiente e localiza um maximo  da corrente */
					
					fprintf(bif, "%.13lf %.13lf\n", V0, R*Ia); 
					nummax++;
				}
				if (nummax>MAXMAX) {
					break;
				}
	//			if ((cont>cutb)&&(Va<V)&&(Va<Vaa)&&(nummax<MAXMAX))
		/* corta o transiente e localiza um minimo da tensao */
	//				{
	//				  fprintf(bif,"%.13lf %.13lf\n",frequencia,Va); 
	//				  nummax++;
	//				}
	//			if ((cont>itermin)&&(V>Vc)/*&&(dV<dVc)*/) stop=1;
	//			}
	//		if ((somaV!=0.0 )&&(somaI!=0.0 ))
	//		  fprintf(med,"%.13lf %.13lf %#lg\n", freq,
	//			  somaV/(cont-contini),somaI/(cont-contini));
	//		  else 
	//		    {
	//		      fprintf(med,"# constante em:\n");
	//		      fprintf(med,"%.13lf %.13lf %#lg\n", freq, Va, I);
	//		    }
			}//end for
			printf("\n V0 = %.13lf", V0);
	//		fflush(med);
			fflush(bif);
		}//end for
	//	fclose(med);
		fclose(bif);
		tempo1 = time(NULL);
		printf("\n %s: Calculo completo em %f segundos.\n", argv[0], difftime(tempo1, tempo0));
		printf("Arquivo: %s\n", nomebif);
	//	printf("Arquivos: %s e %s\n", nomebif, nomemed);
	return(0);
}//end main
