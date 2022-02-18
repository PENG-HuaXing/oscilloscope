#include<fstream>
#include<iostream>
#include<vector>
using namespace std;

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
	return 0;
}
