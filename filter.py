#!/usr/bin/python
import numpy as np
import pylab as pl
import sys

'''
A really simple IIR filter, and not that flexible
'''
class IIR:
	'''
	b is x-coefficients
	a is y-coefficients
	b is of length (filter order + 1)
	a is of length (filter order + 1)( ie assumes a[0], which is ommitted, would be 1.0)
	'''
	def __init__(self,_b,_a):
		self.b = _b
		self.a = _a[1:len(_a)]	#just omit first element
		print self.a
		if (_a[0] != 1.0):
			print "ERROR IMPLEMENT NORMALIZATION"
			sys.exit(1)
		self.outs = [0]*len(self.a)
		self.ins = [0]*len(self.b)

	def input(self,i):
		self.ins.insert(0,i)	#push new item
		del self.ins[-1]	#delete last item
		sum1 = np.dot(self.ins,self.b)
		sum2 = np.dot(self.outs,self.a)
		self.outs.insert(0,sum1-sum2)
		del self.outs[-1]

	def getOutput(self):
		return self.outs[0]	



if __name__ == '__main__':
	filt = IIR([5.542717e-03,  -1.108543e-02,   5.542717e-03],[1.0000000,   1.7786318,   0.8008026])
	output = []
	input = []
	for i in range(0,100):
		filt.input( 1 if i==0 else 0)
		input.append(1 if i==0 else 0)
		print filt.getOutput()
		output.append(filt.getOutput())
	pl.plot(output)
	pl.show()
