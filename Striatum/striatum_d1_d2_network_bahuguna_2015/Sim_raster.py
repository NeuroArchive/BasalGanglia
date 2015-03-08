
# Author: Jyotika Bahuguna:- j.bahuguna@fz-juelich.de

import numpy as np
import matplotlib.cm as cm
import pickle
import sys
import itertools
import matplotlib
#matplotlib.use('Agg')
import pylab as pl
from matplotlib.font_manager import FontProperties
import pickle
import sys
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import params as p
fontP = FontProperties()

pars = p.get_parameters()

# Reads from the pickle files generated by generateFig4.py
def getSimdata():

	Rates = pickle.load(open("Rates_Fig4_.pickle","r"))
	
	return Rates


# Plot the Rasters for two example cortical rates (before and after DTT)
def plotRaster(ax1,Rate,figL):
	evsAll = pickle.load(open("Senders_Fig4_.pickle","r"))
	tsAll = pickle.load(open("Times_Fig4_.pickle","r"))

	ratelist = pars.Rate
	ind1 = np.where(np.abs(pars.Rate-float(Rate))<0.5)
	
	evs = dict()
	ts = dict()

	evs['ctx'] = evsAll['ctx'][ind1[0]]
	evs['d1'] = evsAll['d1'][ind1[0]]
	evs['d2'] = evsAll['d2'][ind1[0]]
	evs['fsi'] = evsAll['fsi'][ind1[0]]

	ts['ctx'] = tsAll['ctx'][ind1[0]]
	ts['d1'] =  tsAll['d1'][ind1[0]]
	ts['d2'] =  tsAll['d2'][ind1[0]]
	ts['fsi'] = tsAll['fsi'][ind1[0]]

	# Print a smaller snapshot of simulation, 60 msecs
	stoptime=80
	binsize=2.
	starttime = 20
	binning = np.arange(starttime,stoptime,binsize)
	ind = np.where(ts['d1']<=stoptime)
	semi_ts = ts['d1'][ind]
	semi_evs = evs['d1'][ind]

	ax1.plot(semi_ts,semi_evs,'b.',label='D1',markersize=4)

	ind = np.where(ts['d2']<=stoptime)
	semi_ts = ts['d2'][ind]
	semi_evs = evs['d2'][ind]
	ax1.plot(semi_ts,semi_evs,'r.',label='D2',markersize=4)
	ax1.set_yticks([1,2000,4000])
	ax1.set_yticklabels(['0','2k','4k'],fontsize=10,fontweight='bold')#,fontsize=8,stretch='ultra-condensed')

	for i in ax1.get_xticklabels():
		i.set_fontsize(10)
		i.set_visible(False)
		i.set_fontweight('bold')
	ax1.set_ylabel(' Neuron ID',fontsize=12,fontweight='bold',fontname='Computer Modern')

	ax1.set_xlim(starttime,stoptime)
	ax1.text(12,4700.5,figL,fontsize=14,fontweight='bold',fontname='Computer Modern')	
	divider = make_axes_locatable(ax1)	

	ax2 = divider.append_axes("bottom", size="100%", pad=0.0)  # To makes subplots stick to each other but not others
	ind = np.where(ts['d1']<=stoptime) and np.where(ts['d1'] > 10.0)
	a1,b1 = np.histogram(ts['d1'][ind],binning)
	ind = np.where(ts['d2']<=stoptime) and np.where(ts['d2'] > 10.0)
	a2,b2 = np.histogram(ts['d2'][ind],binning)
	sizeInsecs = binsize/1000.
	ax2.step(b1[:-1],(a1/2000.)/sizeInsecs,'b-',label='D1',linewidth=1.5)
	if Rate == str(4050.0):
		ax2.step(b1[:-1],(a2/1800.)/sizeInsecs,'r-',label='D2',linewidth=1.5)
	else:
		ax2.step(b1[:-1],(a2/2000.)/sizeInsecs,'r-',label='D2',linewidth=1.5)
	
	mud1 = np.mean(((a1/2000.)/0.2))
	mud2 = np.mean(((a2/2000.)/0.2))
	ax2.set_xlim(starttime,stoptime)
	print "mud1",mud1
	print "mud2",mud2

	ax2.set_xlim(starttime,stoptime)
	for i in ax2.get_xticklabels():
		i.set_fontsize(10)
		i.set_visible(False)
		i.set_fontweight('bold')
	for i in ax2.get_yticklabels():
		i.set_visible(False)

	for i in ax2.get_yticklabels()[1::3]:
		i.set_fontsize(10)
		i.set_fontweight('bold')
		i.set_visible(True)
	ax2.set_xlabel('Time(ms)',fontsize=12,fontweight='bold',fontname='Computer Modern')
	ax2.set_ylabel('Rate(Hz)',fontsize=12,fontweight='bold',fontname='Computer Modern')

	ax3 = divider.append_axes("bottom", size="100%", pad=0.0)  # To makes subplots stick to each other but not others
	ax3.step(b1[:-1],((a1/2000.)-(a2/2000.))/sizeInsecs,'k-',label='$\lambda_{D1}$-$\lambda_{D2}$',linewidth=1.5)
	ax3.hlines(0,starttime,stoptime,colors='k',linestyle='dashed')
	ax3.set_xlim(starttime,stoptime)
	ax3.set_ylim(-6,6)
	for i in ax3.get_xticklabels():
		i.set_fontsize(10)
		#i.set_visible(False)
		i.set_fontweight('bold')
	for i in ax3.get_yticklabels():
		i.set_visible(False)

	for i in ax3.get_yticklabels()[1::3]:
		i.set_fontsize(10)
		i.set_fontweight('bold')
		i.set_visible(True)
	ax3.set_xlabel('Time(ms)',fontsize=12,fontweight='bold',fontname='Computer Modern')
	ax3.set_ylabel('$\Delta_{MSN}$',fontsize=13,fontweight='bold',fontname='Computer Modern')


def drawFig4():

	fig2 = plt.figure(figsize=(6.5,6.5))
	ax42 = plt.subplot2grid((2,2),(0,0),rowspan=2)
	Rates = getSimdata()
	t421 = ax42.plot(np.array(Rates['ctx']),Rates['d1'],'bo-',label='$\lambda$-D1',markersize=9,linewidth=1.5)[0]
	t422 = ax42.plot(np.array(Rates['ctx']),Rates['d2'],'ro-',label='$\lambda$-D2',markersize=9,linewidth=1.5)[0]
	for i in ax42.get_yticklabels():
		i.set_color('b')
		i.set_fontsize(12)
		i.set_fontweight('bold')
	ax42.set_ylabel('$\lambda$-D1,D2 (Hz)',fontsize=14,color='b',fontname='Computer Modern',fontweight='bold')
	ax42.vlines(16.7,ymin=0,ymax=4.3,linestyles='dashed')
	ax42.hlines(4.3,xmin=0,xmax=16.7,linestyles='dashed')
	ax42.set_xlim(0.0,35)
	ax42.set_ylim(0.0,12)
	ax42.set_yticks([0,2,4,6,8,10,12])
	ax421 = ax42.twinx()
	t431 = ax421.plot(np.array(Rates['ctx']),Rates['fsi'],'go-',label='$\lambda$-FSI',markersize=9,linewidth=1.5)[0] # [0] required for legend, or it gives an error
	for i in ax421.get_yticklabels():
		i.set_color('g')
		i.set_fontsize(12)
		i.set_fontweight('bold')
	ax421.set_ylabel('$\lambda$-FSI (Hz)',fontsize=14,color='g',fontname='Computer Modern',fontweight='bold')		
	ax421.set_ylim(0,80)

	ax42.set_xlabel('$\lambda$-Ctx (Hz)',fontsize=14,fontname='Computer Modern',fontweight='bold')
	for i in ax42.get_xticklabels():
		i.set_fontsize(12)
		i.set_fontweight('bold')
	i = ax42.get_xticklabels()[-1]
	i.set_visible(False)
	ax421.set_xlim(0.,35.0)	
	ax421.legend((t421,t422,t431),('D1','D2','FSI'),loc='best',prop=fontP)




	B = str(0.01)
	W = str(0.01)

	#======================================4050.0============
	ax43 = plt.subplot2grid((4,2),(0,1),rowspan=2)
	Rate = str(4050.0)
	#Rate = str(4550.0)
	plotRaster(ax43,Rate,"(b)")
	point1 = np.where(pars.Rate==float(Rate))[0]

	ax45 = plt.subplot2grid((4,2),(2,1),rowspan=2)
	Rate = str(1050.0)
	point2 = np.where(pars.Rate==float(Rate))[0]
	plotRaster(ax45,Rate,"(a)")

	ax42.text(11.,7.2,"(b)",fontweight='bold',fontsize=15,fontname='Computer Modern')

	ax42.plot(Rates['ctx'][point1],Rates['d1'][point1],marker='o',markersize=7,markerfacecolor='w',markeredgecolor='k')
	ax42.plot(Rates['ctx'][point1],Rates['d2'][point1],marker='o',markersize=7,markerfacecolor='w',markeredgecolor='k')
	fig2.tight_layout(pad=1.9, w_pad=3.8, h_pad=1.5)

	ax42.text(3,3.2,"(a)",fontweight='bold',fontsize=15,fontname='Computer Modern')
	ax42.plot(Rates['ctx'][point2],Rates['d1'][point2],marker='o',markersize=7,markerfacecolor='w',markeredgecolor='k')
	ax42.plot(Rates['ctx'][point2],Rates['d2'][point2],marker='o',markersize=7,markerfacecolor='w',markeredgecolor='k')



	plt.savefig('IpVsOpSimred.pdf')
	pl.show()


