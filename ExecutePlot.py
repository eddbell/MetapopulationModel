#!/usr/bin/env python3
import matplotlib.pyplot as plt,numpy as np
import csv
import os, signal, sys, argparse

def sgn(signal,frame):
    sys.exit(0)
signal.signal(signal.SIGINT,sgn)

def plot(num,namefile):

    #read data
    file = open(f"{namefile[int(num)]}.csv",'r')
    reader = csv.reader(x.replace('\0', '') for x in file)
    d = np.array([np.array(i) for i in reader])
    #str to int
    d = np.asarray([np.asarray([int(i) for i in j]) for j in d])
    file.close()

    nsim = len(d)   #number of realization
    print(d)

    y_mean_single = []  #define average
    for i in d.T:
        y_mean_single.append(np.mean(i))


    ax.plot(d[0],linewidth=5,color="gray",alpha =  0.6, label="One realization")
    ax.plot(y_mean_single,linewidth=5,color="black",label=f"Average over {nsim} realizations")
    ax.set_xlabel("Time (generations)");
    ax.set_ylabel("Diversity (S)")

    ax.legend(prop={'size': 20},frameon=False)
    plt.savefig(f"{namefile[int(num)]}.pdf")
    plt.show()
    return 0

def boxplot(num,namefile):

    #read data
    file = open(f"{namefile[int(num)]}.csv",'r')
    reader = csv.reader(x.replace('\0', '') for x in file)
    d = np.array([np.array(i) for i in reader])
    #str to int
    d = np.asarray([np.asarray([float(i) for i in j]) for j in d])
    file.close()

    nsim = len(d)   #number of realization
    print(nsim)

    values = []
    for i in d:
        values.append(i)

    ax.boxplot(values, positions = w_list,widths = 0.3, meanline=False,showmeans=False,labels=w_list,zorder = 1)
    ax.set_xlabel("w/w0 (Frequency)");
    ax.set_ylabel("S (Diversity)")

    ax.legend(prop={'size': 20},frameon=False)
    plt.savefig(f"{namefile[int(num)]}.pdf")
    plt.show()
    return 0

#define variables
namefile = []
num = 0
w_list =(0.1, 0.5, 1, 3, 7, 10)#(0.3,0.6,0.9,1.1,1.5,2.,3.,4.,5.,8.)
#define plot
fig = plt.figure(figsize=(8,8))
ax = plt.axes()

#selection process of the file
dir_path = os.path.dirname(os.path.realpath(__file__))
for f in os.listdir(dir_path):
    name, ext = os.path.splitext(f)
    if ext == '.csv':
        namefile.append(os.path.splitext(f)[0])
        print(f"{name}\t\t {num}")
        num = num + 1
try:
    sys.argv[1]
except:
    num= input("Insert number of the file : ")
else:
    num = sys.argv[1]

#recognise kind of file
vars = namefile[int(num)].split("_")[0]

#execute plot
if vars == "f": boxplot(num,namefile)
else:   plot(num,namefile)
