/* Diagrama de bifurcacao e media das equacoes para
Oscilador Nao-linear com diodo

Calculado por metodo de Runge-Kutta de quarta ordem        */

# include <stdlib.h>
# include <stdio.h>
# include <math.h>
# define dim 3
# define d 6.0e-8     /* dt    */

# define freqinicial 62.67000e3  /*12.0e3*/
# define freqfinal 62.91500e3

// numero de me'dias temporais calculadas no intervalo [Ainicial,Afinal]
# define num 100
# define itermin (200000)
# define itermax (250000)
# define cutb    9l*itermin/10l /* 9l*itermin/10l */
# define cutm 1l*(itermin/5l)  
# define MAXMAX 30 /*50*/
# define Vc 3e-3
# define dVc 4e-3 /* 0.3 */
//# define Ic 0.0


# define Cs0 6e-13 /* 1.46880e-14 */ /* 10e-13 */
# define Cj0 1.850e-11
# define phi 0.0420
# define Phi 0.750
# define L 1e-1
# define R 1.0e3 /* 500.0L */
# define V0 2.700 /*1e-1*/
# define I0 4.8e-9 

# define Vi 0.01
# define Ii 0.00001
# define thetai 0.0

void getname (char [256]);

FILE *med;                  /*   freq <V> <I> */
FILE *bif;                  /*   freq max(I)  */
double omega;
double freq;


void /*int*/ getname(char name[256])
	{
	printf(" Entre com o nome do arquivo a ser gravado: ");
	scanf("%s",name);
	printf("\n");
	/* return(1); */
	}

/* equacoes auxiliares */
double Id(double I0inter, double Vinter, double phiinter)
{
  return I0inter*(exp(Vinter/phiinter)-1);
}

double Cs(double Cs0int, double Vint, double phiint)
{
  //if (Vint>0.0)
    return Cs0int*exp(Vint/phiint);
    //else return Cs0int;
}
double Cj(double Cj0int, double Vint, double Phiint)
{
  //if (Vint<0.0)
    return Cj0int/sqrt(1.0-Vint/Phiint);
    //else return Cj0int;
}
double C(double Cs0int, double Cj0int, double Vint,
	      double phiint, double Phiint)
{
  return Cs(Cs0int, Vint, phiint)+Cj(Cj0int, Vint, Phiint);
}

/* funcoes das equacoes diferenciais  */

double fI(double Iint,double Vint,double thetaint)
	{
	return (V0*sin(thetaint) - R*Iint - Vint)/L;
	}
double fV(double Iint,double Vint,double thetaint)
	{
	return (Iint-Id(I0,Vint,phi))/C(Cs0,Cj0,Vint,phi,Phi);
	}
double ftheta()
	{
	return omega;
	}

int main (argc,argv)
	char *argc, **argv;
	{
	char nomemed [256],nomebif [256] ;
	long cont,contini;
	int start,stop,nummax;
	double k1[dim],k2[dim],k3[dim],k4[dim];
//k1I,k2I,k3I,k4I,k1U,k2U,k3U,k4U,k1W,k2W,k3W,k4W,k1Ub,k2Ub,k3Ub,k4Ub;
	//	double I [3],U,W,Ub;
	double I=Ii, V=Vi, theta=thetai,Va=0.0,Vaa=0.0, Ia=0.0, Iaa=0.0;
	double step,t;
	double somaV, somaI, dVa=0.0, dV=0.0;  

	printf("\r\n");
	printf("\tUsando frequencia como parametro de controle\n");
	printf("\tEquacoes para Oscilador Nao-linear usando Diodo \n\n");
	printf("\t\t dV/dt = (I-Id)/C\n");
	printf("\t\t dI/dt = [V0 sen(omega t) -RI -V]/L  \n");
	printf("\t\t dteta/dt = omega \n");
	printf("\t\t Id = I0exp(V/phi)-1\n");
	printf("\t\t C = Cj+Cs\n");
	printf("\t\t Cj = Cj0(1-V/Phi)^(-1/2)\n");
	printf("\t\t Cs = Cs0exp(V/phi)\n\n");
	printf("\n");

	printf(" Para as médias,\n");
 	getname(nomemed);
	med = fopen(nomemed,"wt");
	printf(" Para o diagrama de bifurcação,\n");
	getname(nomebif);
	bif = fopen(nomebif,"wt");  
	printf(" Iniciando o calculo \r\n");
	//	for (j=0;j<3;I[j++]=Ii); U=Ui; W=Wi; Ub=Ubi; 
	//step=(omegafinal-omegainicial)/num;
	step=(freqfinal-freqinicial)/num;
	Va=0.0; I=0.0;
	fprintf(bif,"# freqini=%.13lf\n# freqfinal=%.13lf\n",
		freqinicial, freqfinal);
	fprintf(med,"# freqini=%.13lf\n# freqfinal=%.13lf\n",
		freqinicial, freqfinal);
	for (freq=freqinicial; freq<freqfinal; freq+=step)
		{		  
		somaV=0.0 ;
		somaI=0.0 ;
		t=0.0 ;
		omega= 6.2831853071795862*freq;
		start=0; stop=0; nummax=0;
		for (cont=0l;(cont<=itermax)&&(!stop);cont++)
			{
			/* as linhas abaixo constituem o algoritmo de Runge-Kutta de quarta ordem */
			k1[0]=d*fI(I,V,theta);
			k1[1]=d*fV(I,V,theta);
			k1[2]=d*ftheta(I,V,theta);

			k2[0]=d*fI(I+k1[0]/2.0,V+k1[1]/2.0,theta+k1[2]/2.0);
			k2[1]=d*fV(I+k1[0]/2.0,V+k1[1]/2.0,theta+k1[2]/2.0);
			k2[2]=d*ftheta(I+k1[0]/2.0,V+k1[1]/2.0,theta+k1[2]/2.0);
			
			k3[0]=d*fI(I+k2[0]/2.0 ,V+k2[1]/2.0 ,theta+k2[2]/2.0 );
			k3[1]=d*fV(I+k2[0]/2.0 ,V+k2[1]/2.0 ,theta+k2[2]/2.0 );
			k3[2]=d*ftheta(I+k2[0]/2.0 ,V+k2[1]/2.0 ,theta+k2[2]/2.0 );

			
			k4[0]=d*fI(I+k3[0],V+k3[1],theta+k3[2]);
			k4[1]=d*fV(I+k3[0],V+k3[1],theta+k3[2]);
			k4[2]=d*ftheta(I+k3[0],V+k3[1],theta+k3[2]);

			dVa=dV;
			dV=(k1[1]+2.0 *k2[1]+2.0 *k3[1]+k4[1])/6.0 ;

			Iaa=Ia;
			Ia=I;

			I+=(k1[0]+2.0 *k2[0]+2.0 *k3[0]+k4[0])/6.0 ;
			theta+=(k1[2]+2.0 *k2[2]+2.0 *k3[2]+k4[2])/6.0 ;
			t+=d;

			Vaa=Va;
			Va=V;
			V+=dV;
			if ((start==0)&&(cont>cutm)&&(V>Vc)&&(fabs(dV)<dVc))
				{
				start=1;
				contini=cont;
				}
			if (start) 
			  {
			    somaV+=V;
			    somaI+=I;
			  }

/*			if ( (cont>cutb)&&(Ia>I)&&(Ia>Iaa)&&(nummax<MAXMAX) )*/
          /* corta o transiente e localiza um maximo  da corrente */
/*				{
				  fprintf(bif,"%.13lf %.13lf\n",freq,Ia); 
				  nummax++;
				} */
			if ( (cont>cutb)&&(Va<V)&&(Va<Vaa)&&(nummax<MAXMAX) )
          /* corta o transiente e localiza um minimo da tensao */
				{
				  fprintf(bif,"%.13lf %.13lf\n",freq,Va); 
				  nummax++;
				}
			if ((cont>itermin)&&(V>Vc)/*&&(dV<dVc)*/) stop=1;
			}
		if ((somaV!=0.0 )&&(somaI!=0.0 ))
		  fprintf(med,"%.13lf %.13lf %#lg\n", freq,
			  somaV/(cont-contini),somaI/(cont-contini));
		  else 
		    {
		      fprintf(med,"# constante em:\n");
		      fprintf(med,"%.13lf %.13lf %#lg\n", freq, Va, I);
		    }
		printf("\n freq=%.13lf",freq);
		fflush(med);
		fflush(bif);
		}
	fclose(med);
  	fclose(bif);
	printf("\n %s: Calculo completo.\n",argv[0]); 
	printf(" Arquivos: %s e %s\n",nomebif, nomemed);
	return (0);
	}
