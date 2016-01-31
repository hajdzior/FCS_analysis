#import matplotlib libary
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import *
from os import listdir
from os.path import isfile, join
import re # Regular expres.
#import matplotlib.gridspec as gridspec
#import matplotlib.pyplot as plt
#import sFCS_data, getopt 



def utnij(filename):
  return filename[4:filename.find("au")]

def read_pars_trip(file_now, k):
	pars = []
	f = open (file_now, "rt")
	l = f.readline()
	l = f.readline()
	while l:
		va = l.split()
		if va[0] == names[k]:
			pars.append(float(va[3])) #rho
		l = f.readline()
	print pars
	return pars
#----------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++

mypath ='./FCSs'
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
print files

cmap = plt.get_cmap('jet_r')
N = len(files)
if len(files) != 1:
	files.sort(key = lambda file_name: [float(re.search('(\d+)au', file_name).group(1))])

au_now = -1. 
c_num = -1.
for fn in range(len(files)):	
	pars_files_trip = ['trip/' + files[fn][0:files[fn].find("-FCSs")] + '-trip.dat']
	inputfile = mypath + '/' + files[fn]
	print inputfile
	
	f = open (inputfile, "rt")
	l = f.readline()
	res_names = l.split()
	if len(files) == 1:
		N = len(res_names)
	#sort by excitation laser power
	res_names.sort(key = lambda name_now: [float(re.search('(\d+)au', name_now).group(1))])
	l = f.readline()
	is_times = l.split('\t')
	f.close()
	data = np.loadtxt(inputfile, skiprows=2)
	FCS_data = data.transpose()
	for nn in range(0,len(is_times)-1):#
		if (is_times[nn] == "G(t)[10{^-3}]"):
			FCS_data[nn] = [y/1000 for y in FCS_data[nn]]

	fig1 = figure(1, figsize=(10,5))
	fig2 = figure(2, figsize=(10,5))

	aus = [float(re.search('(\d+)au', name_now).group(1)) for name_now in res_names]
	uW = [au*0.074 for au in aus]
	for k in range(0,len(res_names)-1): # how many plots from this parameter set
		if aus[k] != au_now:
			au_now = aus[k]
			lab = str("%.2f" % uW[k]) + '$\mu$W'
			c_num = c_num + 1.
			color = cmap(c_num/N)
			fig=figure(1)
			plt.plot(FCS_data[0], FCS_data[k*3+1], label = lab, c = color)
			fig=figure(2)
			plt.plot(FCS_data[0], FCS_data[k*3+1], label = lab, c = color)
		else:
			plt.plot(FCS_data[0], FCS_data[k*3+1], c = color)
	if len(files) != 1:
		plt.legend(loc='best')
		plt.xlim(0.001,100.)
		plt.xscale('log')
		plt.ylim(-0.,1.1)
		plt.ylabel('FCS')
		plt.xlabel('$\ tau$')
		plt.legend(ncol=3, loc='best', 
		columnspacing=1.0, labelspacing=0.0,
		handletextpad=0.0, handlelength=1.5,
		fancybox=True, shadow=True)# bbox_to_anchor=[0.5, 1.1]
		f_name = 'plots-FCSs/' + re.search('(\d+)au', name_now).group(1) + '.png'
		print f_name
		plt.savefig(f_name)
		plt.clf()

fig=figure(1)		
plt.legend(loc='best')
plt.xlim(0.001,100.)
plt.xscale('log')
plt.ylim(-0.,5.1)
plt.ylabel('FCS')
plt.xlabel('$\ tau$')
plt.legend(ncol=3, loc='best', 
columnspacing=1.0, labelspacing=0.0,
handletextpad=0.0, handlelength=1.5,
fancybox=True, shadow=True)# bbox_to_anchor=[0.5, 1.1]
f_name = 'plots-FCSs/all.png'
print f_name
plt.savefig(f_name)

#plt.clf()

#for k in range(0,len(names)-1): # how many plots from this parameter set
	#color = cmap(float(fn)/N)
	#rho = read_pars_trip(pars_files_trip[fn], k)
	#lab = str("%.2f" % uW[k]) + '$\mu$W'
	##textt = textt + names[k][19:-6] + '[au]\n'
	##print textt
	#FCS_n = [y/rho for y in FCS_data[k*3+1]]
	#if k == len(names)-2:
		#plt.plot(FCS_data[0], FCS_n, label = lab, c = color)
	#else:
		#plt.plot(FCS_data[0], FCS_n, c = color)
		## Inset
#plt.legend(loc='best')
#plt.xlim(0.001,100.)
#plt.xscale('log')
#plt.ylim(-0.,1.05)
#plt.ylabel('FCS, norm')
#plt.xlabel('$\ tau$')
#plt.legend(ncol=3, loc='best', 
#columnspacing=1.0, labelspacing=0.0,
#handletextpad=0.0, handlelength=1.5,
#fancybox=True, shadow=True)# bbox_to_anchor=[0.5, 1.1]
#f_name = 'plots-FCSs/all-norm.png'
#plt.savefig(f_name)
	
