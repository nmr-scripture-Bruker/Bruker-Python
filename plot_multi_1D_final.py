#
# Topspin Python API example
#
# Copyright (c) 2022
# Bruker BioSpin GmbH
#
# This program will plot multiple 1D 1H NMR
# All desire spectra has to be in the same directory
# The first spectrum that you want to export must be loaded in topspin
#

from bruker.api.topspin import Topspin
from bruker.data.nmr  import *
from datetime import datetime
from matplotlib import pyplot as plt
import numpy
import sys
import array


#
# Demonstrates the use of the Topspin REST interface
#
top = Topspin()
dp = top.getDataProvider()
H_spectrum =dp.getCurrentDataset()


############Global Variable ####################
expno = []
multi_plot = []

######### Pre define function ###################
def collect_spectra(H_temp = dp ,spectra=[],exp=[],index=0):
    index = 0
    for i in expno:
        print("collecting spectrum in Experiment "+str(expno[index]))
        H_temp.launch("re "+str(expno[index]))
        H_temp =dp.getCurrentDataset()
        specData_temp = H_temp.getSpecDataPoints()
        index = index +1
        spectra.append(specData_temp['dataPoints'])

print(type(H_spectrum))
print("This is a program that plot mulitple 1D for publication & Figure ")
print("How many spectra you plan on plotting? :")
num_plot = input()
print("------------------------------------------")
print("Are those spectra number continuouly or not? (type Y or N)")
answer = input()
print("------------------------------------------")

if answer == 'y':
    print("What is the expno of your first spectrum")
    first_expno = input()
    expno_i = int(first_expno)
    for i in range(int(num_plot)):
        expno.append(expno_i)
        expno_i = expno_i +1
else:
    print("Enter each expno that you want to print")
    for i in range(int(num_plot)):
        expno_temp = input()
        expno.append(expno_temp)

print("Enter the ppm range you want to plot?")
print("Enter Left limit: ")
l_ppm = float(input())
print("Enter right limit: ")
r_ppm = float(input())
num =1
collect_spectra(H_spectrum,multi_plot,expno,index=0)


# necessary to inverse the x axis (NMR standard)
#plt.xlim(left,right)


######## setting up all the subplot ################
index = 0
num = 1

for i in expno:
     plt.subplot(int(num_plot),1,int(num))
     specData = H_spectrum.getSpecDataPoints()
     pr = specData['physicalRanges'][0]
     left = float(pr['start'])
     right = float(pr['end'])
     plt.xlim(l_ppm,r_ppm)
     axis = numpy.linspace(left,right,len(specData['dataPoints']))
 
     plt.plot(axis,multi_plot[index])
     ax = plt.gca()
     ax.spines['top'].set_visible(False)
     ax.spines['right'].set_visible(False)
     ax.spines['bottom'].set_visible(True)
     ax.spines['left'].set_visible(False)
     ax.get_yaxis().set_visible(False)
     ax.get_xaxis().set_visible(True)
     num = num +1
     index = index +1

plt.show()


