#!/usr/bin/env python3
import matplotlib.pyplot as plt,numpy as np
import csv
import os, signal, sys, argparse

def sgn(signal,frame):
    sys.exit(0)
signal.signal(signal.SIGINT,sgn)

def plot(num,nomefile):

    #read data
    file = open(f"{nomefile[int(num)]}.csv",'r')
    reader = csv.reader(x.replace('\0', '') for x in file)
    d = np.array([np.array(i) for i in reader])
    #str to int
    d = np.asarray([np.asarray([int(i) for i in j]) for j in d])
    file.close()

    nsim = len(d)   #number of the realizations
    print(d)

    y_mean_single = []  #define average array
    for i in d.T:
        y_mean_single.append(np.mean(i))

    ax.plot(d[0],linewidth=5,color="gray",alpha =  0.6, label="One realization")
    ax.plot(y_mean_single,linewidth=5,color="black",label=f"Average over {nsim} realizations")
    
    ax.set_xlabel("Time (generations)");
    ax.set_ylabel("Diversity (S)")
    ax.tick_params(axis="both",which='major', width=1.0,direction = "in", labelsize=30)
    ax.tick_params(axis="both",which='major', length=10,direction = "in", labelsize=30)
    ax.yaxis.label.set_size(30)
    ax.xaxis.label.set_size(30)
    ax.legend(prop={'size': 20},frameon=False)
    
    plt.savefig(f"{nomefile[int(num)]}.pdf")
    plt.show()
    return 0

nomefile = []
num = 0

fig = plt.figure(figsize=(9,9))
ax = fig.add_subplot()

dir_path = os.path.dirname(os.path.realpath(__file__))
for f in os.listdir(dir_path):
    name, ext = os.path.splitext(f)
    if ext == '.csv':
        nomefile.append(os.path.splitext(f)[0])
        print(f"{name}\t\t {num}")
        num = num + 1
try:
    sys.argv[1]
except:
    num= input("Insert the number of the file : ")
else:
    num = sys.argv[1]

plot(num,nomefile)
