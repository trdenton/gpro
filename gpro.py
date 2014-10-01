#!/usr/bin/python
from scipy.io import wavfile
import numpy as np
import sys
import pylab as pl
from filter import IIR


if len(sys.argv) < 2:
	print "Error - need to provide wav file...."
	sys.exit(0)

filename = sys.argv[1]

fs,sound = wavfile.read(filename)


l = sound[:,0]
r = sound[:,1]

print "Total samples: %d" % len(l)
print "Sample freq: %d" % fs


#we want 10ms of data at a time
numSampsPerChunk = int(fs*0.01)

nBins = numSampsPerChunk
dF = fs/nBins
print "Frequency resolution is: %f Hz" % dF

print "we have %f chunks" % (len(l)/numSampsPerChunk)

LInt = np.zeros([(numSampsPerChunk)/2])
RInt = np.zeros([(numSampsPerChunk)/2])
dL = np.zeros([(numSampsPerChunk)/2])
dR = np.zeros([(numSampsPerChunk)/2])

LOld = None
ROld = None

sumDs = [] #sum derivative
sumPs = [] #sum proportional
sumFs = [] #sum filterd

b = [9.747574e-04,   2.924272e-03,   2.924272e-03,   9.747574e-04]
a = [1.0000000,  -2.5766530,   2.2382739,  -0.6538228]

filt = IIR(b,a)
for i in range(0,int(  len(l)/numSampsPerChunk  )):
	lChunk = l[i*numSampsPerChunk : min((i+1)*numSampsPerChunk,len(l))]
	rChunk = r[i*numSampsPerChunk : min((i+1)*numSampsPerChunk,len(r))]
	L = np.fft.fft(lChunk)
	R = np.fft.fft(rChunk)
	#we only need half of fft output

	L = L[len(L)/2:len(L)-1]
	R = R[len(R)/2:len(R)-1]

	L = map(abs,L)
	R = map(abs,R)


	#calculate integrals
	LInt += L
	RInt += R


	#calculate derivatives
	if (LOld is not None):
		dL = L - LOld
	else:
		LOld = np.copy(L)
		dL = np.copy(L)

	LOld = np.copy(L)
	if (ROld is not None):
		dR = R - ROld
	else:
		ROld = np.copy(R)
		dR = np.copy(R)

	#we only need to analyze one channel at the moment...

	sumP = np.sum(L)
	sumD = np.sum(dL)

	#lets only take a look at the upper half of the spectrum, a string hit will manifest itself mostly in brief high frequency content

	sumP = np.sum(L[  int(0.95*len(L)):len(L)])
	sumD = abs(np.sum(dL[  int(0.95*len(dL)):len(dL)]))

	sumDs.append(sumD)	
	filt.input(sumD)
	sumFs.append(filt.getOutput())
	sumPs.append(sumP)	

pl.subplot(411)
pl.plot(sumPs)
pl.subplot(412)
pl.plot(sumDs)
pl.subplot(413)

#do some ghetto BPF
SUMDS = np.fft.fft(sumDs)
halfway = len(SUMDS)/2
width = int(0.45*len(SUMDS))
SUMDS[halfway-width:halfway+width]=0
sumDs = np.fft.ifft(SUMDS)

pl.plot(abs(sumDs))

pl.subplot(414)
pl.plot(sumFs)
pl.show()
	
	
