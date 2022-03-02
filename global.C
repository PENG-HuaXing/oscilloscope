#include<fstream>
#include<iostream>
#include<vector>
#include "TMath.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TF1.h"
using namespace std;

double S_ped_noise(double *xx, double *par)
{
	//par[0] is w
	//par[1] is alpha
	//par[2] is poisson mu
	//par[3] is gauss mean q0
	//par[4] is gauss sigma sigma0
	double x = xx[0];
	double term1;
	if (x > par[3])
	{
		term1 = par[0] * par[1] * TMath::Exp(-par[1] * (x-par[3]));
	}
	else
	{
		term1 = 0;
	}
	double term2 = (1-par[0]) * TMath::Gaus(x, par[3], par[4], true);
	return (term1 + term2) * TMath::Poisson(0, par[2]);
}
double S_ped_noise_scale(double *xx, double *par)
{
	//par[0] is w
	//par[1] is alpha
	//par[2] is poisson mu
	//par[3] is gauss mean q0
	//par[4] is gauss sigma sigma0
	//par[5] is scale
	double x = xx[0];
	double term1;
	if (x > par[3])
	{
		term1 = par[0] * par[1] * TMath::Exp(-par[1] * (x-par[3]));
	}
	else
	{
		term1 = 0;
	}
	double term2 = (1-par[0]) * TMath::Gaus(x, par[3], par[4], true);
	return (term1 + term2) * TMath::Poisson(0, par[2]) * par[5];
}

double S_ped(double *xx, double *par)
{
	//par[0] is poisson mu;
	//par[1] is gauss mean;
	//par[2] is gauss sigma;
	double x = xx[0];
	double term1 = TMath::Gaus(x, par[1], par[2], true);
	return term1 * TMath::Poisson(0, par[0]);
}

double S_nspe(double *xx, double *par)
{
	//par[0] is poisson mu
	//par[1] is ped gauss mean
	//par[2] is signal gauss mean(q1)
	//par[3] is signal gauss sigma(sigma1)
	int n = 4;
	double x = xx[0];
	double value = 0;
	for(int i=1; i<=n; ++i)
	{
		value += TMath::Poisson(i, par[0]) * TMath::Gaus(x, par[1] + i * par[2], TMath::Sqrt(i) * par[3], true);
	}
	return value; 
}

double S_nspe_qsh(double *xx, double *par)
{
	//par[0] is w
	//par[1] is alpha
	//par[2] is poisson mu
	//par[3] is ped gauss mean(q0)
	//par[4] is signal gauss mean(q1)
	//par[5] is signal gauss sigma(sigma1)
	//qsh = w/alpha = par[0]/par[1]
	int n = 4;
	double x = xx[0];
	double value = 0;
	for(int i=1; i<=n; ++i)
	{
		value += TMath::Poisson(i, par[2]) * TMath::Gaus(x, par[3] + par[0]/par[1] + i * par[4], TMath::Sqrt(i) * par[5], true);
	}
	return value; 
}
double S_nspe_qsh_scale(double *xx, double *par)
{
	//par[0] is w
	//par[1] is alpha
	//par[2] is poisson mu
	//par[3] is ped gauss mean(q0)
	//par[4] is signal gauss mean(q1)
	//par[5] is signal gauss sigma(sigma1)
	//par[6] is scale
	//qsh = w/alpha = par[0]/par[1]
	int n = 4;
	double x = xx[0];
	double value = 0;
	for(int i=1; i<=n; ++i)
	{
		value += TMath::Poisson(i, par[2]) * TMath::Gaus(x, par[3] + par[0]/par[1] + i * par[4], TMath::Sqrt(i) * par[5], true);
	}
	return value * par[6]; 
}
double S_spe(double *xx, double *par)
{
	//par[0] is poisson mu
	//par[1] is ped gauss mean
	//par[2] is signal gauss mean(q1)
	//par[3] is signal gauss sigma(sigma1)
	//par[4] is n photon
	//par[5] is q_sh
	double x = xx[0];
	int n = par[4];
	double value = TMath::Poisson(n, par[0]) * TMath::Gaus(x, par[1] + n * par[2], TMath::Sqrt(n) * par[3], true);
	return value; 
}
double global_fun(double * xx, double * par)
{
	// par[0] is amp
	// par[1] is poisson mu
	// par[2] is ped q0
	// par[3] is ped sigma0
	// par[4] is signal q1
	// par[5] is signal sigam1
	double par1[3] = {par[1], par[2], par[3]};
	double par2[4] = {par[1], par[2], par[4], par[5]};
	double ped = S_ped(xx, par1);//par = {mu, q0, sigma0}
	double signal = S_nspe(xx, par2);//par = {mu, q0, q1, sigma1}
	return (ped + signal) * par[0];
}
double global_fun_noise(double * xx, double * par)
{
	// par[0] is amp
	// par[1] is w
	// par[2] is alpha
	// par[3] is poisson mu
	// par[4] is ped q0
	// par[5] is ped sigma0
	// par[6] is signal q1
	// par[7] is signal sigam1
	double par1[5] = {par[1], par[2], par[3], par[4], par[5]};
	double ped = S_ped_noise(xx, par1);//par = {w, alpha, mu, q0, sigma0}
	double par2[6] = {par[1], par[2], par[3], par[4], par[6], par[7]};
	double signal = S_nspe_qsh(xx, par2);//par = {w, alpha, mu, q0, q1, sigma1}
	return (ped + signal) * par[0];
}

int global_fit()
{
	gStyle->SetOptFit(1111);
	auto f = new TF1("f", global_fun, -3, 25, 6);//无指数噪声模型
	auto f_noise = new TF1("f_noise", global_fun_noise, -3,3, 8);//含有指数噪声模型
	vector<double> data; 
	double a;
	ifstream infile;
	infile.open("./example/histogram_qdc.txt", ios::in);
	for(;infile.good();)
	{
		infile >> a;
		data.push_back(a);
	}
	double start_bin = 940;
	double end_bins = 1200;
	auto h = new TH1D("h", "h", int(end_bins-start_bin), start_bin, end_bins);
	for(size_t i=0;i<data.size();i++)
	{
		h->Fill(data.at(i));
	}
	//******************2022_2_25_CR160_data拟合初值设置*********************************
	//f->SetParameters(3.1e2, 6e-1, 1e-1, 4e-1, 4, 1);
	//f_noise->SetParameters(3e4, 0.4, 0.6, 0.6, 0, 0.5, 4.5, 1.5);
	//f_noise->SetParLimits(3, 0.2, 0.8);//mu
	//f_noise->SetParLimits(4, -0.5, 0.5); //q0
	//f_noise->SetParLimits(5, 0, 2); //sigma0
	//f_noise->SetParLimits(6, 4, 6);//q1
	//f_noise->SetParLimits(7, 0, 10);//sigma1
	//***********************************************************************************
	//*********CR160_-1450V_LED_1KHz_3.7V_32ns_V965_CH1.txt初值设置**********************
	//f->SetParameters(2e4, 0.4, 950, 1, 37, 16);
	f_noise->SetParameters(2.77e4, 0.4, 0.06, 1.094, 955, 1.733, 30, 11.05);
	//f_noise->SetParLimits(3, 0.2, 0.8);//mu
	//f_noise->SetParLimits(4, -0.5, 0.5); //q0
	//f_noise->SetParLimits(5, 0, 2); //sigma0
	//f_noise->SetParLimits(6, 4, 6);//q1
	//f_noise->SetParLimits(7, 0, 10);//sigma1
	//***********************************************************************************

	//h->Fit(f);//拟合无指数噪声的模型
	h->Fit(f_noise);//拟合带有指数噪声的模型
	//double * fit_par = new double [8];
	//f_noise->GetParameters(fit_par);
	//auto f_ped = new TF1("f_ped", S_ped_noise, -5,10, 5);
	//f_ped->SetParameters(fit_par[1], fit_par[2], fit_par[3], fit_par[4], fit_par[5]);
	//f_ped->SetLineColor(kBlue);
	//auto f_signal = new TF1("f_signal", S_nspe_qsh, 0, 80, 6);
	//f_signal->SetParameters(fit_par[1], fit_par[2], fit_par[3], fit_par[4], fit_par[6], fit_par[7]);
	//f_signal->SetLineColor(kGreen);
	//auto c2 = new TCanvas("c2", "c2", 800, 600);
	//f_signal->Draw("C");
	//for (int i =0;i<8;i++)
	//{
		//std::cout << fit_par[i] << std::endl;
	//}
	auto c1 = new TCanvas("c1", "c1", 800, 600);
	h->Draw();
	return 0;
}
