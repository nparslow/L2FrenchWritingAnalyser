from matplotlib import mlab

__author__ = 'nparslow'



import json
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os
import xml.etree.cElementTree as ET



x = np.linspace(1, 10001)
y = np.power(x, -1)

def SfunctionAltLogist(x, b, x0, k):
    # need to convert x to a float?
    #print x
    #if s > 0 :
        #print s
        #print x

    #z = mlab.normpdf(x,0,1000)
    return  100*(1.0-np.log( 1 + np.power(x,b))*(1/(1+np.exp(-k*(x-x0)))))
    #return np.convolve(z,y)

y = SfunctionAltLogist(x, -0.25, 5000.0, 0.00001)


plt.figure()
plt.plot(x, y, 'ko', label="data")
#plt.plot(ranks, func(ranks, *popt), 'r-', label="Fitted Curve")
#plt.legend(loc='lower right')
plt.show()
#print popt
