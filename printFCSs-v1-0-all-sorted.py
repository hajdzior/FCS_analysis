#import matplotlib libary
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pylab import *
from os import listdir
from os.path import isfile, join
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
			#pars.append(float(va[5])) #tauD
			#pars.append(float(va[7])) #T
			#pars.append(float(va[9])/1000) #tauT
			#pars.append(float(va[11])) #kappa
		l = f.readline()
	print pars
	return pars
#----------------------------------------------------------
#++++++++++++++++++++++++++++++++++++++++++

mypath ='./FCSs'
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
print files


#colormap = plt.cm.gist_ncar
#plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, len(files))])
#print colormap
	
cmap = plt.get_cmap('jet_r')
N = len(files)
files.sort(key = lambda name: float(name[name.find("s3_")+3:name.find("au_")]))
#import pdb; pdb.set_trace()

for fn in range(len(files)):	
	color = cmap(float(fn)/N)
	pars_files_trip = ['trip/' + files[fn][0:files[fn].find("-FCSs")] + '-trip.dat']
	
	inputfile = mypath + '/' + files[fn]
	print inputfile
	
	f = open (inputfile, "rt")
	l = f.readline()
	names = l.split()
	l = f.readline()
	is_times = l.split('\t')
	f.close()
	data = np.loadtxt(inputfile, skiprows=2)
	FCS_data = data.transpose()
	for nn in range(0,len(is_times)-1):#
		if (is_times[nn] == "G(t)[10{^-3}]"):
			FCS_data[nn] = [y/1000 for y in FCS_data[nn]]
	#textt = 'laser power: \n'
		
	
	fig=figure(1, figsize=(10,5))
	fig2=figure(2, figsize=(10,5))
	#num_plots = len(files)
	#print num_plots
	# Have a look at the colormaps here and decide which one you'd like:
	# http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
	aus = [float(name[name.find("p50_")+4:name.find("au_")]) for name in names]
	uW = [au*0.074 for au in aus]
	for k in range(0,len(names)-1): # how many plots from this parameter set
		#print k
		#lab = names[k][19:-6] + '[au]'
		lab = str("%.2f" % uW[k]) + '$\mu$W'
		#textt = textt + names[k][19:-6] + '[au]\n'
		#print textt
		fig=figure(1)
		if k == 0:
			plt.plot(FCS_data[0], FCS_data[k*3+1], label = lab, c = color)
		#else:
			#plt.plot(FCS_data[0], FCS_data[k*3+1], c = color)
			
		fig=figure(2)
		if k == 0:
			plt.plot(FCS_data[0], FCS_data[k*3+1], label = lab, c = color)
		else:
			plt.plot(FCS_data[0], FCS_data[k*3+1], c = color)
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
	f_name = 'plots-FCSs/' + name[name.find("p50_")+4:name.find("au_")] + '.png'
	print f_name
	plt.savefig(f_name)
	plt.clf()

fig=figure(1)		
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
	
