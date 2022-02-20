#include<fstream>
#include<iostream>
#include<vector>
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
using namespace std;

double S_noise(double *xx, double *par)
{
	double x = xx[0];
	double term1 = par[0]*par[1]*TMath::Exp(-par[1]*x);
	double term2 = (1-par[0]) * TMath::Gaus(x, par[2], par[3]);
	return term1 + term2;
}

double S_ped(double *xx, double *par)
{
	double x = xx[0];
	return TMath::Exp(par[0]) * TMath::Gaus(x, par[1], par[2]);
}

double S_spe(double *xx, double *par)
{
	double x = xx[0];
	return TMath::Poisson(1, par[0]) * TMath::Gaus(x, par[1], par[2]);
}
int global_fit()
{
	vector<double> x, y;
	double a1, a2;
	ifstream infile;
	infile.open("scatter.txt", ios::in);
	for(;infile.good();)
	{
		infile >> a1;
		infile >> a2;
		x.push_back(a1);
		y.push_back(a2);
	}
	for(size_t i=0;i<x.size();i++)
	{
		cout << x.at(i) << "\t" << y.at(i) << endl;
	}
	double par_noise[4] = {0.392, 38.7, 450.7, 8.941};
	TF1 * f_noise =new TF1("f_noise",S_noise , 400, 750, 4);
	f_noise->SetParameters(&par_noise[0]);
	f_noise->Draw();

	return 0;
}
