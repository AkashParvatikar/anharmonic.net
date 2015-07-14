import MDAnalysis
import numpy
import numpy.linalg
import math
from KabschAlign import *

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class IterativeMeansAlign(object):
	
	def __init__(self):
		"""
		Constructor
		"""

	def iterativeMeans(self, coords, eps, maxIter, verbose):
		# all coordinates are expected to be passed as a (Ns x 3 x Na)  array
		# where Na = number of atoms; Ns = number of snapshots
	
		# This file has been edited to produce identical results as the original matlab implementation.

		Ns = numpy.shape(coords)[0]; if verbose: print Ns; 
		dim = numpy.shape(coords)[1]; if verbose: print dim;
		Na = numpy.shape(coords)[2]; if verbose: print Na;
		
		avgCoords = [];			# track average coordinates
		kalign = KabschAlign();		# initialize for use

		ok = 0;				# tracking convergence of iterative means
		itr = 1; 			# iteration number
		
		eRMSD = [];
		
		while not(ok):
			tmpRMSD = [];
			mnC = numpy.mean(coords, 0); 
			avgCoords.append(mnC);
			for i in range(0,Ns):
				fromXYZ = coords[i];
				[R, T, xRMSD, err] = kalign.kabsch(mnC, fromXYZ, i);
				tmpRMSD.append(xRMSD); 
				tmp = numpy.tile(T, Na);
				pxyz = numpy.dot(R,fromXYZ) + tmp;  
				coords[i] = pxyz;
			eRMSD.append(numpy.array(tmpRMSD).T);
			newMnC = numpy.mean(coords,0); 
			err = math.sqrt(sum( (mnC.flatten()-newMnC.flatten())**2) )
			if val.verbose: print("Iteration #%i with an error of %f" %(itr, err))
			if err <= eps or itr == maxIter:
				ok = 1;
			itr = itr + 1;
		return [itr,avgCoords,eRMSD,coords];

if __name__=='__main__':
	u = MDAnalysis.Universe('../data/ubq_1111.pdb', '../data/UBQ_500ns.dcd', permissive=False);
	ca = u.selectAtoms('name CA');
	cacoords = []; frames = [];
	for ts in u.trajectory:
		f = ca.coordinates();
		cacoords.append(f.T);
		frames.append(ts.frame);
	print numpy.shape(cacoords);
	
	iterAlign = IterativeMeansAlign();
	[itr, avgCoords, eRMSD, newCoords] = iterAlign.iterativeMeans(cacoords, 0.001, 4, True); 
	
	print numpy.shape(eRMSD);
	newCoords = numpy.array(newCoords);
	newCoords = numpy.reshape(newCoords, (10000,3*69)); print numpy.shape(newCoords); 
	fig = plt.figure();
	ax = fig.add_subplot(111);
	ax.plot(frames, eRMSD[1], linestyle='solid', linewidth=2.0);
	plt.show();
