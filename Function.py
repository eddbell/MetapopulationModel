import numpy as np
from Model import mod
import os, signal, sys, csv, scipy
from scipy.stats import expon

#Deletes the simulations file if you stop the process (CTRL+C)
def sgn(signal,frame):
    os.remove(filename)
    sys.exit(0)

#deletes the final comma in simulations
def DeleteComma(data):
    data.seek(0,2) # end of file
    size=data.tell() # the size...
    data.truncate(size-1)
    return 0

#simulation of neutral model. OUTPUT: diversity per generation
def DiversityNeutral(nsim,N,nu):

    global filename
    filename = f'{N}_{nu}_{nsim}_neutral_model.csv'
    signal.signal(signal.SIGINT,sgn)

    data = open(filename,'w')
    if nu != 0:  Nmax = int(3 * N / nu)
    for y in range(nsim):
        print("-------------------------------------")
        print(f"\nSimulation {y+1} of {nsim} simulation(s)\n")
        pop = mod(N,nu)
        for k in range(int(Nmax)):
            pop.neutral_model()
            if k%N == 0:
                data.write(f"{pop.diversity(pop.x)},")
        pop.rename_species()

        DeleteComma(data)

        data.write("\n")

    data.close()
    print(filename)
    return 0

#simulations of a meta-population WITH introduction of a gene. OUTPUT: Diversity per generation
def DiversityGene(nsim,N,nu,h,m,g,pi):

    global filename
    filename = f'{nu}_{h}_{pi}_{N}_{g}_{nsim}_diversity_gene.csv'
    signal.signal(signal.SIGINT,sgn)

    data = open(filename,'w')

    if nu != 0:  Nmax = int(N / nu)
    for y in range(nsim):
        print("-------------------------------------")
        print(f"\nSimulation {y+1} of {nsim} simulation(s)\n")

        pop = mod(N,nu)

        for k in range(int(Nmax)):
            pop.neutral_model()
            if k%int(N) == 0:
                data.write(f"{pop.diversity(pop.x)},")
        pop.rename_species()

        pop.generateX()
        print("Introduction of the gene\n")
        for k in range(int(Nmax)):
            pop.gene_model(h,g,pi)
            if k%int(N) == 0:
                data.write(f"{pop.diversity(pop.X)},")
        DeleteComma(data)
        data.write("\n")
    data.close()
    print(filename)
    return

#simulations with multiple gene model. OUTPUT: Diversity per generation
def DiversityMultipleGene(nsim,N,nu,h,m,g,pi,w0):

    global filename
    filename = f'{nu}_{h}_{pi}_{N}_{w0}_{g}_{nsim}_multiple_gene.csv'
    #filename2 = f'0_{nu}_{h}_{pi}_{N}_{w0}_{g}_{nsim}_gene_print.csv'
    signal.signal(signal.SIGINT,sgn)

    N_max = int(50*N / nu)
    data = open(filename,'w')
    #data2 = open(filename2,'w')

    for y in range(nsim):
        print("-------------------------------------")
        print(f"\nSimulation {y+1} of {nsim} simulation(s)\n")
        w = GenFreq(w0,N,m,h)

        pop = mod(N,nu)
        pop.generateX()

        for k in range(N_max):
            pop.multiple_gene_model(h,pi,w)
            if k%int(N) == 0:   #every generation
                data.write(f"{pop.diversity(pop.X)},")
                if k%int(w*N) == 0:
                    #data2.write(f"{k/N},")
                    print(f"{pop.gene_count}-th gene   |  w = ",w)
                    w = GenFreq(w0,N,m,h)

        DeleteComma(data)
        data.write("\n")
        #DeleteComma(data2)
        #data2.write("\n")
    data.close()
    #data2.close()
    print(filename)
    #print(filename2)

#simulations with multiple gene model. OUTPUT: Diversity per w
def DiversityMultipleGenePerFrequency(nsim,N,nu,h,m,g,pi,w0):

    global filename
    filename = f'f_{nu}_{h}_{pi}_{N}_{w0}_{g}_{nsim}_multiple_gene_per_frequency.csv'
    signal.signal(signal.SIGINT,sgn)

    data = open(filename,'w')
    N_max = int(10*N / nu)
    S0 = -N*nu*np.log(nu)
    w_list = (0.1, 0.5, 1, 3, 7, 10)

    print("List of frequencies:  w = ",np.trunc(np.ones(len(w_list))*w0/w_list))
    for f in w_list:

        print(f"\n\nw = ",w0/f)
        for y in range(nsim):
            print("-------------------------------------")
            print(f"\nSimulation {y+1} of {nsim} simulation(s)\n")
            S = 0
            Ns = 0
            w =GenFreq(w0/f,N,m,h)

            pop = mod(N,nu)
            pop.generateX()
            for k in range(N_max):
                pop.multiple_gene_model(h,pi,w)
                if k%int(N) == 0:   #every generation
                    if k%int(w*N) == 0:
                        print(f"{pop.gene_count}-th gene   |  w = ",w)
                        w = GenFreq(w0/f,N,m,h)
                    if  k > int(N / nu):    #Wait the diverisity is stabilized before to catch data
                        S = S + pop.diversity(pop.X)/S0
                        Ns = Ns +1;
            data.write(f"{S/Ns},")
        if k > int(N / nu): DeleteComma(data)
        data.write("\n")
    data.close()
    print(filename)

#extract frequency values from exponential pdf
def GenFreq(w0,N,m,h):
    s = int(np.log(N)/(m+h))  #define very low w values threshore
    w = expon.rvs(loc=s, scale=w0, size=1)[0]
    while w == 0:   w = expon.rvs(loc=s, scale=w0, size=1)[0]

    return int(w)
