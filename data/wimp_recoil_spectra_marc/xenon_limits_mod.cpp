

/////////////////////////////////////////////////////////////////////////
// xenon_limits_mod.cpp
/////////////////////////////////////////////////////////////////////////


/* ----------------------------------------------------------------------
Daniel Baur, 6th February 2020
This is the modified version of the 'xenon_limits.cpp' file.
I used it to automatically generate WIMP recoil spectra for my SFS code (a wrapper framework for NEST).
Therefore I made a few adjustments.
---------------------------------------------------------------------- */


/* ----------------------------------------------------------------------
  Script provides functions to get xenon WIMP spectra (in keVr and PE)
  and to calculate exclusion limits based on the observation of zero events
  
  functions:
    int conversion_keV2pe()  
      -- initialize Leff for PE and Poisson smearing
      
    Double_t diffratefunct(Double_t *x,Double_t *params)
      -- definition of the xenon recoil spectrum (including Formfactor)
      
    double diffrate_int(wimpmass [GeV], sigma [cm^2], plot=1/0, lowBorder [keVr], highBorder [keVr])
      -- plot recoil spectrum in keVr 
         return integral rate (in evts / kg / day) between low and highBorder   
         
    double perate_int(wimpmass [GeV], sigma [cm^2], plot=1/0, lowBorder [keVr], highBorder [keVr])
      -- plot recoil spectrum in PE (with and w/o Poisson smearing)
         return integral rate of Poisson smeared spectrum (in evts / kg / day) between low and highBorder
         
    int limit(exposure [kgxdays], acceptance [1], lowBorder [keVr], highBorder [keVr], display=1,2,3, poiss=1/0)
      -- determine 90% CL limit from exposure and acceptance assuming the observation of 0 events
         30 mass points between 6 GeV/c^2 and 1000 GeV/c^2 are used
         display=1 shows the line, =2 the data, =3 both
         poiss=1/0.. with or without Poisson smearing
-------------------------------------------------------------------------*/





/////////////////////////////////////////////////////////////////////////
// Imports
/////////////////////////////////////////////////////////////////////////


#include "TMath.h"
#include "TF1.h"
#include "TROOT.h"
#include "TVirtualFitter.h"
#include "TStopwatch.h"
#include "TRandom.h"
#include "TMinuit.h"
#include "TGraph.h"
#include "TCanvas.h"
#include <fstream>
#include <iostream> // I uncommented this


using namespace std;





/////////////////////////////////////////////////////////////////////////
// Defining Constants
/////////////////////////////////////////////////////////////////////////


Double_t pi=3.141592654;	// pi
// fundamental constants
Double_t N0=6.02214199e26; 	// Avogadro Constant
Double_t c=299792458.0;     	// vacuum speed of light [m/s]
Double_t mp=0.9382728;     	// mass of the proton [GeV/c^2]
Double_t u=0.93149401;   	// Atomic mass unit [GeV/c^2]
// WIMP halo constants
Double_t v_0=220000.0;       	// real mean velocity of DM Maxewellian distribution [m/s]
Double_t v_esc=544000.0;     	// real escape velocity of DM [m/s]
Double_t v_E=232000.0;       	// real mean velocity of Earth [m/s]
Double_t rho_DM=0.3;       	// local DM density [GeV/cm^3]
// conversion factors
Double_t fmtoGeV=1.0/0.197327; 	// conversion from fm to 1/GeV
Double_t keVtoGeV=1e-6;  	// conversion from keV to GeV
Double_t daytos=60.0*60.0*24.0;	// conversion from day to seconds
Double_t stoday=1.0/daytos;  	//conversion from s to day
Double_t mtocm=1e2;        	//conversion from m to cm
Double_t cm2topbarn=1e36;  	//conversion from cm^2 to picobarn
Double_t pbarntocm2=1e-36; 	//conversion from picobarn to cm^2
Double_t epsilon=1e-10;
// nuclear constants for form factor
Double_t a0=0.52; //fm
Double_t s=0.9;  //fm





/////////////////////////////////////////////////////////////////////////
// Isotopic Composition of Xenon
/////////////////////////////////////////////////////////////////////////


const int nbOfIsotopes=9;
Double_t atoms[nbOfIsotopes]={124.0, 126.0, 128.0, 129.0, 130.0, 131.0, 132.0, 134.0, 136.0};
Double_t nat[nbOfIsotopes]={0.0009, 0.0009, 0.0192, 0.2644, 0.0408, 0.2118, 0.2689, 0.1044, 0.0887};
Double_t atoms_mass[nbOfIsotopes]={123.905, 125.904, 127.903, 128.905, 129.9035, 130.9050, 131.9041, 133.904144, 135.9072};

Double_t sigma, A, natabu, mass;
Double_t Totalrate;
Double_t Ratenuc[nbOfIsotopes];





/////////////////////////////////////////////////////////////////////////
// Definition of Differential Recoil Spectrum Histogram
/////////////////////////////////////////////////////////////////////////


int nbins=600;		// number of bins  -- limits with 600 bins are identical to 1200 bins
			// -- use 120 bins for fast (and less accurate execution of script)
double upper=60.;	// upper histogram limit; Er in keVr
TH1F *diffratehist = new TH1F("diffratehist",";Recoil Energy [keVr];Cnts / keV / kg / day",nbins,0,upper);
TH1F *smearedhist;
TH1F *pehist;
TGraph *glimit;
TGraph *keVtope;
TGraph *petokeV;
TH2D *dmy;


// Create Canvas and define display options
TCanvas *myCan = new TCanvas("myCan","Limits (local)");


// define Poisson distribution 
 double poiss(double x, double mean)
{
  return TMath::Poisson(x,mean);
}





/////////////////////////////////////////////////////////////////////////
// Defining the Conversion Function from keVr to PE (and Back)
/////////////////////////////////////////////////////////////////////////


// -- (XENON100, run_08, best fit, linear extrapolation to zero)
int conversion_keV2pe()
{
  double enr[63]={0.,1.,1.5,2.,2.5,
           3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 
           26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 
           47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60};
  double pe[63]={0,0,0.1734,0.3970,0.6565,
          0.9726, 1.4307, 1.9307, 2.4951, 3.1118, 3.7577, 4.4285, 5.1158, 5.7087, 6.3085, 6.9270, 
          7.5654, 8.2170, 8.8484, 9.4882, 10.1382, 10.7984, 11.4693, 12.1587, 12.8597, 13.5717, 
          14.2948, 15.0293, 15.7807, 16.5441, 17.3191, 18.1056, 18.8996, 19.6290, 20.3604, 21.0979, 
          21.8416, 22.5914, 23.3474, 24.1095, 24.8777, 25.6521, 26.4314, 27.1954, 27.9632, 28.7359, 
          29.5136, 30.2963, 31.0840, 31.8766, 32.6742, 33.4768, 34.2815, 35.0373, 35.7928, 36.5510, 
          37.3118, 38.0752, 38.8413, 39.6100, 40.3814, 41.1554, 41.9297};

  double enr90[34]={0.0, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 
	  9.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 300.0};
  double pe90[34]={0.00000, 0.00000, 0.00000, 0.05423, 0.14187, 0.22990, 0.31849, 0.40778, 0.49786, 0.59871, 0.70403, 
	  0.82067, 1.22639, 1.70413, 2.23841, 2.83156, 3.45432, 4.09169, 4.74127, 5.86466, 7.55773, 10.50420, 13.80085, 
	  17.45784, 24.59815, 32.17987, 39.60673, 46.59781, 53.33738, 59.86931, 66.56542, 79.81580, 93.95537, 199.01845};

  // use mean Leff (run_08)	  
/*  for (int i=0; i<63; i++) pe[i]=pe[i]*3.0/2.2;	  // scale to higher light yield
	  
  keVtope = new TGraph(63,enr,pe);
  petokeV = new TGraph(63,pe,enr);
*/  
  // use lower 90% Leff contour [calculated via Leff90=LeffMean-1.28*(LeffMean-Leff1Sigma)]
  for (int i=0; i<34; i++) pe90[i]=pe90[i]*3.0/2.2;	  // scale to higher light yield
	  
  keVtope = new TGraph(34,enr90,pe90);
  petokeV = new TGraph(34,pe90,enr90);
  
  return 0;
}





/////////////////////////////////////////////////////////////////////////
// Defining the Differential WIMP Spectrum for a 1 pb = 1e-36 cm^2 Xsection
/////////////////////////////////////////////////////////////////////////


//   x[0] = recoil energy Er
//   params = contain information on target and WIMP mass
//          [0] = A -- nucleon number of target iotope
//          [1] = natural abundance of target isotope 
//          [2] = target mass   [u]
//          [3] = Wimp mass     [in GeV/c^2] 
//          [4] = cross section [in cm^2]


Double_t diffratefunct(Double_t *x,Double_t *params)
{
	Double_t diffrateval, munucwimp, mupwimp, E0 ,r ,c0 ,rn, F, k1_k0, R0, vmin, velocityint;
	Double_t m_wimp=params[3];
	Double_t sig=params[4];
	
	// reduced masses
	munucwimp=m_wimp*u*params[2]/(m_wimp+u*params[2]);
	mupwimp=m_wimp*mp/(m_wimp+mp);
	
	// mean kinetic energy of WIMP
	E0=0.5*1.e6*m_wimp*TMath::Power(v_0/c,2.0);   // 1/2 mv^2 and 1e6 is conversion from GeV to keV	
	// kinematic factor
	r=4.0*m_wimp*u*params[2]/TMath::Power((m_wimp+u*params[2]),2.0);	
	
	// Formfactor -----------------------------------------------------------------
	// variables
	c0=1.23*TMath::Power(params[0],1.0/3.0)-0.6; //fm
	rn=sqrt(TMath::Power(c0,2.0)+7.0/3.0*TMath::Power(pi,2.0)*TMath::Power(a0,2.0)-5.0*TMath::Power(s,2.0));
	// FF definition
	F=3.0*(sin(sqrt(2.0*u*params[2]*x[0]*keVtoGeV)*rn*fmtoGeV)-(sqrt(2.0*u*params[2]*x[0]*keVtoGeV)*rn*fmtoGeV)
	     *cos(sqrt(2.0*u*params[2]*x[0]*keVtoGeV)*rn*fmtoGeV))/TMath::Power(sqrt(2.0*u*params[2]*x[0]*keVtoGeV)*rn*fmtoGeV,3.0)
	     *exp(-1.0/2.0*TMath::Power((sqrt(2.0*u*params[2]*x[0]*keVtoGeV)*s*fmtoGeV),2.0));		
	//------------------------------------------------------------------------------

	// Velocity integral -----------------------------------------------------------
	// minimum velocity to generate recoil Er=x[0]
	vmin=sqrt(x[0]/(E0*r))*v_0;
	// k-factor for normaization
	k1_k0=1.0/(TMath::Erf(v_esc/v_0)-2.0/sqrt(pi)*v_esc/v_0*exp(-TMath::Power(v_esc,2.0)/TMath::Power(v_0,2.0)));  	
	
	// velocity integral
	// -- separation in the different energy bins see Savage et al, JCAP  04 (2009) 010, or Sebastian's PhD thesis
	// -- if the standard L&S approach should be used, the first if clause should be changed to "if (0.0<vmin && vmin<=(v_esc+v_E))"
	//    and evergything else should be removed
	if (0.0<vmin && vmin<=(v_esc-v_E))
	{
	  velocityint=(sqrt(pi)/4.0*v_0/v_E*(TMath::Erf((vmin+v_E)/v_0)-TMath::Erf((vmin-v_E)/v_0))-exp(-TMath::Power(v_esc/v_0,2.0)));
	}
	else if((v_esc-v_E)<vmin && vmin<=(v_esc+v_E))
	{
	  velocityint=(sqrt(pi)/4.0*v_0/v_E*(TMath::Erf(v_esc/v_0)-TMath::Erf((vmin-v_E)/v_0))-(v_esc+v_E-vmin)/(2.0*v_E)*exp(-TMath::Power(v_esc/v_0,2.0)));
	}
	else{velocityint=1e-200;}
	//------------------------------------------------------------------------------

	// Rate determination ----------------------------------------------------------
	// uncorrected Rate
	R0=2.0/sqrt(pi)*N0/params[2]*rho_DM/m_wimp*pbarntocm2*TMath::Power(params[0],2.0)*TMath::Power(munucwimp,2.0)/
	       TMath::Power(mupwimp,2.0)*v_0*mtocm*daytos*sig*cm2topbarn;
	// differential rate
	diffrateval=R0*params[1]*k1_k0*(1.0/(E0*r))*velocityint*TMath::Power(F,2.0);
	//------------------------------------------------------------------------------

	return diffrateval;
}





/////////////////////////////////////////////////////////////////////////
// Generating WIMP Spectrum in PE and Apply Poisson Smearing
/////////////////////////////////////////////////////////////////////////


// -- [uses Leff definition coded in conversion_keV2pe()]
// -- return integral (in cnts / kg / day) between lowBorder and highBorder (in keVr, conversion to PE is done automatically)
// -- plot a histogram with the differential WIMP spectrum in PE (smeared and unsmeared)
// -- it has been verified that the WIMP rate integral from the PE (unsmeared) spectrum agrees with the keV spectrum withing <1%
//    wimpmass  = WIMP mass [GeV/c^2]
//    sigma     = cross section [cm^2]
//    plot      = 1 .. display spectrum, 0 .. don't display
//    lowBorder = lower analysis range [keVr]
//    highBorder= upper analysis range [keVr]


double perate_int(double wimpmass, double sigma, int plot, double lowBorder, double highBorder)
{
  // determine recoil spectrum (in keVr) for a given WIMP mass and cross section
  TF1 *diffrate=new TF1("diffratefunct",diffratefunct,0.0,200,5);
  diffrate->SetName("diffrate");

  // define recoil histogram in PE ---------------------------------------------
  conversion_keV2pe();
  double upp=keVtope->Eval(upper);
  upp=48.;
  pehist = new TH1F("pehist",";Energy [PE];Cnts / PE / kg / day",nbins,0,upp);
  
  double left,right;
  double pleft,pright;
  for(int k=1;k<nbins;k++) {
    pleft=pehist->GetBinLowEdge(k);
    pright=pehist->GetBinLowEdge(k)+pehist->GetBinWidth(k);
    left=petokeV->Eval(pleft);
    right=petokeV->Eval(pright);
    
    for(int j=0;j<nbOfIsotopes;++j) {
      A=atoms[j];
      natabu=nat[j];
      mass=atoms_mass[j];
      Ratenuc[j]=0.0;
      
      diffrate->SetParameters(A,natabu,mass,wimpmass,sigma);
      Ratenuc[j]=(diffrate->Eval(right)+diffrate->Eval(left))/2.*(right-left);
    }
    Totalrate=(Ratenuc[0]+Ratenuc[1]+Ratenuc[2]+Ratenuc[3]+Ratenuc[4]+Ratenuc[5]+Ratenuc[6]+Ratenuc[7]+Ratenuc[8]);	
    if (Totalrate<0.) Totalrate=0.;
    pehist->SetBinContent(k,Totalrate/(pright-pleft));  
  }  
  
  // now smear histogram ------------------------------------------------------
  TF1 *fp = new TF1 ("fp","poiss(x,[0])",0,80);
  smearedhist = new TH1F("smearedhist",";Energy [PE];Cnts / PE / kg / day",nbins,0,upp);

  TH1F *hh = new TH1F("hh","",nbins,0,upp);
  double intg, val, weight;
  for (int i=1; i<=nbins; i++) {
    fp->SetParameter(0,pehist->GetBinCenter(i));
    weight=pehist->GetBinContent(i);
    intg=0.;
    for (int j=1; j<nbins; j++) {
      val=fp->Eval(hh->GetBinCenter(j));
      hh->SetBinContent(j,val);
      intg+=val;
    }
    hh->Scale(weight/intg);
    smearedhist->Add(hh);    
  }  

  // plot spectra if requested ------------------------------------------------
  if (plot==1) { 
    char str[100];
    sprintf(str,"Xe: %d GeV/c^{2} WIMP Recoil Spectrum",(int)wimpmass);
    pehist->SetTitle(str);
    pehist->SetLineColor(2);
    pehist->SetLineWidth(2);
    pehist->Draw();
    smearedhist->SetLineWidth(2);
    smearedhist->Draw("same");
  }  

  // calculate integral of smeared spectrum ------------------------------------
  lowBorder=keVtope->Eval(lowBorder);
  highBorder=keVtope->Eval(highBorder);
  if (lowBorder >= highBorder) return 0.;
  if (lowBorder <0.) lowBorder=0.;
  if (highBorder>upp) { highBorder=upp; printf("WARNING: upper border set to %.1f PE\n",highBorder); }
  
  int lowBin=pehist->FindBin(lowBorder);
  int highBin=pehist->FindBin(highBorder);
  double nbBins=(double)(highBin-lowBin);
//  val = pehist->Integral(lowBin,highBin)/nbBins*(highBorder-lowBorder); 
  val = smearedhist->Integral(lowBin,highBin)/nbBins*(highBorder-lowBorder);

  // clean up to avoid warnings
  if (smearedhist) {delete smearedhist; smearedhist = NULL;}
  if (pehist) {delete pehist; pehist = NULL;}
  if (hh) {delete hh; hh = NULL;}
  
  // return integral of smeared spectrum
  return val;
}





/////////////////////////////////////////////////////////////////////////
// Returning Integral and Plotting Histogram ---> This is the Function I Modified Below
/////////////////////////////////////////////////////////////////////////


// return integral (in cnts / kg / day) between lowBorder and highBorder (in keVr)
// plot a histogram with the differential WIMP spectrum
//    wimpmass  = WIMP mass [GeV/c^2]
//    sigma     = cross section [cm^2]
//    plot      = 1 .. display spectrum, 0 .. don't display
//    lowBorder = lower analysis range [keVr]
//    highBorder= upper analysis range [keVr]
double diffrate_int(double wimpmass, double sigma, int plot, double lowBorder, double highBorder)
{
  // determine recoil spectrum for a given WIMP mass and cross section
  TF1 *diffrate=new TF1("diffratefunct",diffratefunct,0.0,200,5);
  diffrate->SetName("diffrate");

  for(int k=0;k<nbins;k++) {	
    for(int j=0;j<nbOfIsotopes;++j) {
      A=atoms[j];
      natabu=nat[j];
      mass=atoms_mass[j];

      Ratenuc[j]=0.0;
      diffrate->SetParameters(A,natabu,mass,wimpmass,sigma);

      Ratenuc[j]=diffrate->Eval(diffratehist->GetBinCenter(k));
    }
    Totalrate=(Ratenuc[0]+Ratenuc[1]+Ratenuc[2]+Ratenuc[3]+Ratenuc[4]+Ratenuc[5]+Ratenuc[6]+Ratenuc[7]+Ratenuc[8]);	
    diffratehist->SetBinContent(k,Totalrate);  
  }  
   
  // plot spectrum if requested ------------------------------------------------
  if (plot==1) { 
    char str[100];
    sprintf(str,"Xe: %d GeV/c^{2} WIMP Recoil Spectrum",(int)wimpmass);
    diffratehist->SetTitle(str);
    diffratehist->SetLineColor(4);
    diffratehist->SetLineWidth(2);
    diffratehist->Draw();
  }  

  // calculate integral ---------------------------------------------------------
  if (lowBorder >= highBorder) return 0.;
  if (lowBorder <0.) lowBorder=0.;
  if (highBorder>upper) { highBorder=upper; printf("WARNING: upper border set to %.1f keVr\n",highBorder); }
  
  int lowBin=diffratehist->FindBin(lowBorder);
  int highBin=diffratehist->FindBin(highBorder);
  double nbBins=(double)(highBin-lowBin);
  return diffratehist->Integral(lowBin,highBin)/nbBins*(highBorder-lowBorder);
  
  return 0;
}





/////////////////////////////////////////////////////////////////////////
// 90% CL Sensitivity Curve
/////////////////////////////////////////////////////////////////////////


// get a 90% CL sensitivity curve (for a given exposure and a flat acceptance)
// -- assume observation of zero events
//   display = 1 .. plot limit
//           = 2 .. output values as table
//           > 1 .. do both
//           = 0 .. do nothing
//   poiss   = 0/1 .. without or with Poisson smearing (uses Leff)


int limit(double exposure, double acceptance, double lowBorder, double highBorder, int display, int poiss)
{
  double mass[30], sig[30];
  // define mass points
  for (int i=0; i<8; i++) mass[i]=6+i;			// to 13 GeV/c^2 -- 1 GeV spacing
  for (int i=8; i<17; i++) mass[i]=14+(i-8)*2;		// to 30 GeV/c^2 -- 2 GeV spacing
  for (int i=17; i<25; i++) mass[i]=35+(i-17)*5; 	// to 70 GeV/c^2 -- 5 GeV spacing
  mass[25]=85.; mass[26]=100.; mass[27]=200.; mass[28]=500.; mass[29]=1000.;
  
  // parse through masses and calculate limit
  double rate;
  for (int i=0; i<30; i++) {
    for (int j=0; j<30-i; j++) printf("*"); printf("\n");
    if (!poiss) rate=diffrate_int(mass[i], 1.e-44, 0, lowBorder, highBorder)*exposure*acceptance;
           else rate=perate_int(mass[i], 1.e-44, 0, lowBorder, highBorder)*exposure*acceptance;
    if (rate<=0) sig[i]=1.e-30;
            else sig[i]=2.3/rate*1.e-44;	// 90% CL;   replace by 3.00 for 95% CL
  } 

  // how to display the result
  if (display==1 || display==3) {
    // display styles
    gStyle->SetOptStat(0000000);
    gStyle->SetTitleFillColor(0);
    gStyle->SetTitleBorderSize(0);
    gStyle->SetStatColor(0);
    gStyle->SetCanvasBorderMode(0);
    gStyle->SetPalette(1);
    myCan->SetBorderMode(0);
    myCan->SetFillColor(0);
    myCan->SetFrameBorderMode(0);
    
    dmy = new TH2D("dmy","",10,mass[0]-1,mass[29],10,1e-48,1e-40);    
    dmy->GetXaxis()->SetTitle("WIMP Mass [GeV/c^{2}]");
    dmy->GetYaxis()->SetTitle("Cross Section [cm^{2}]");
    dmy->Draw();
    myCan->SetLogx();
    myCan->SetLogy();

    // plot graph
    glimit = new TGraph(30,mass,sig);
    glimit->SetName("glimit");
    glimit->SetLineColor(4);
    glimit->SetLineWidth(2);
    glimit->Draw("l same");
  } 
  if (display>1) {
    // output values
    printf("# Wimp Mass [GeV/c^2]   Cross Section [cm^2]\n");
    for (int i=0; i<30; i++) printf("%4d %1.2e\n",(int)mass[i],sig[i]);
  }

  return 0;  
}





/////////////////////////////////////////////////////////////////////////
// Returning WIMP Recoil Spectrum
/////////////////////////////////////////////////////////////////////////


// return integral (in cnts / kg / day) between lowBorder and highBorder (in keVr)
// plot a histogram with the differential WIMP spectrum
//    wimpmass  = WIMP mass [GeV/c^2]
//    sigma     = cross section [cm^2]
//    plot      = 1 .. display spectrum, 0 .. don't display
//    lowBorder = lower analysis range [keVr]
//    highBorder= upper analysis range [keVr]


std::vector<double> wimpspec(double wimpmass, double sigma, int plot, double lowBorder, double highBorder)
{
  // determine recoil spectrum for a given WIMP mass and cross section
  TF1 *diffrate=new TF1("diffratefunct",diffratefunct,0.0,200,5);
  diffrate->SetName("diffrate");

  // Modified by Daniel
  std::vector<double> vec_wimpspectrum;

  for(int k=1;k<=nbins;k++) {	
    for(int j=0;j<nbOfIsotopes;++j) {
      A=atoms[j];
      natabu=nat[j];
      mass=atoms_mass[j];

      Ratenuc[j]=0.0;
      diffrate->SetParameters(A,natabu,mass,wimpmass,sigma);

      Ratenuc[j]=diffrate->Eval(diffratehist->GetBinCenter(k));
    }
    Totalrate=(Ratenuc[0]+Ratenuc[1]+Ratenuc[2]+Ratenuc[3]+Ratenuc[4]+Ratenuc[5]+Ratenuc[6]+Ratenuc[7]+Ratenuc[8]);	
    diffratehist->SetBinContent(k,Totalrate);  

  // Modified by Daniel
  //vec_wimpspectrum.push_back(k);
  vec_wimpspectrum.push_back(diffratehist->GetBinCenter(k));
  vec_wimpspectrum.push_back(Totalrate);

  }  
   
  // plot spectrum if requested ------------------------------------------------
  if (plot==1) { 
    char str[100];
    sprintf(str,"Xe: %d GeV/c^{2} WIMP Recoil Spectrum",(int)wimpmass);
    diffratehist->SetTitle(str);
    diffratehist->SetLineColor(4);
    diffratehist->SetLineWidth(2);
    diffratehist->Draw();
  }  

  return vec_wimpspectrum;
}





/////////////////////////////////////////////////////////////////////////
// Doing Modified Stuff
/////////////////////////////////////////////////////////////////////////


//int xenon_limits_mod(double wimpmass, double wimpcrosssection) 
int xenon_limits_mod(double wimpmass, double wimpcrosssection) 
{
	// defining the output file
	ofstream outputFile;
	outputFile.open("./input_spectra/wimp_recoil_spectrum_histdata.json");

	// generating the wimp spectrum
    std::vector<double> output_vec_wimpspectrum;
	output_vec_wimpspectrum = wimpspec(wimpmass,wimpcrosssection,1,5,50);

	// printing the values of the output vector
    for(int i=0;i<output_vec_wimpspectrum.size();i++) {	
      cout << output_vec_wimpspectrum[i] << "\n";
    }  

	// writing to the output file
	// ---> explanatory text
	char line[250];
    //outputFile << "# This file was generated with 'xenon_limits_mod.cpp'. \n";
	//sprintf(line, "# It contains the histogram data of recoil spectrum of a WIMP of mass %f Gev/c^2 and cross-section %e 1/cm^2.\n", wimpmass, wimpcrosssection);
    //outputFile << line;
    //outputFile << "# Each of the sublists below contains both the recoil energy in keV (bin center) and the corresponding differential rate in cts/keV_r/kg/day.\n\n";
    //outputFile << "wimp_spectrum_histogram = [\n";
    outputFile << "[\n";
	// ---> looping over the output (all but the last two entries)
    for(int i=0;i<(0.5*output_vec_wimpspectrum.size())-1;i++) {	
		char data_line[250];
		sprintf(data_line, "\t[%f,%e],\n", output_vec_wimpspectrum[2*i], output_vec_wimpspectrum[(2*i)+1]);
        outputFile << data_line;
    }
	// ---> including also the last two entries (in order to not print the final ",")
	char data_line[250];
	sprintf(data_line, "\t[%f,%e]\n", output_vec_wimpspectrum[(output_vec_wimpspectrum.size()-2)], output_vec_wimpspectrum[(output_vec_wimpspectrum.size()-1)]);
    outputFile << data_line;
	// ---> closing the .json list
    outputFile << "]";

	// end: closing the output file and returning
	outputFile.close();
    return 0;

}










