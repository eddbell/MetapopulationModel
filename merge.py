#!/usr/bin/env python3
import matplotlib.pyplot as plt,numpy as np
import csv
import os, signal, sys, argparse

def sgn(signal,frame):
    sys.exit(0)
signal.signal(signal.SIGINT,sgn)

#deletes the final comma in simulations
def DeleteComma(data):
    data.seek(0,2) # end of file
    size=data.tell() # the size...
    data.truncate(size-1)
    return 0

def plot(num,nomefile):

    lista_w =(0.1, 0.4, 0.7, 1, 3, 6, 9)#(0.5,1.,2.,4.,6.)#(0.3,0.6,0.9,1.1,1.5,2.,3.,4.,5.,8.)

    def steadydiversity(N,nu):
        x = -N*nu*np.log(nu)
        return x

    #read data
    data = open("MergeS.csv","w")
    for k in range(6):
        row = []
        for n in range(num):
            print("num",num)
            file = open(f"{nomefile[int(n)]}.csv",'r')
            reader = csv.reader(x.replace('\0', '') for x in file)
            d = np.array([np.array(i) for i in reader])
            #str to int
            d = np.asarray([np.asarray([float(i) for i in j]) for j in d])
            file.close()

            row.append(d[k])

        for i in row:
            for j in i:
                data.write(f"{j},")
        DeleteComma(data)
        data.write("\n")
    data.close()
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

plot(num,nomefile)
