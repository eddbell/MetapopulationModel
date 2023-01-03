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

#change name of the file if it already exist.
def ChangeName(nomefile):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = dir_path+f"/{nomefile}"

    # Check whether the path is a file
    while os.path.isfile(path+".csv")== 1:
        nom = nomefile.split('+')
        print(nom)
        nomefile = nom[0]+f"+{int(nom[1])+1}"
        path = dir_path+f"/{nomefile}"

    print("File name:  ", nomefile,".csv")
    return nomefile+".csv"

#simulation of neutral model. OUTPUT: diversity per generation
def DiversityNeutral(nsim,N,nu):

    global filename
    filename = f'{N}_{nu}_{nsim}_neutral_model+0'
    filename = ChangeName(filename)
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
    filename = f'{nu}_{h}_{pi}_{N}_{g}_{nsim}_diversity_gene+0'
    filename = ChangeName(filename)
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
def DiversityMultipleGene(nsim,N,nu,h,m,g,pi,w0,NGI):

    global filename
    filename = f'{nu}_{h}_{pi}_{N}_{w0}_{g}_{nsim}_multiple_gene+0'
    filename = ChangeName(filename)
    signal.signal(signal.SIGINT,sgn)

    data = open(filename,'w')
    S0 = -N*nu*np.log(nu)

    for y in range(nsim):
        print("-------------------------------------")
        print(f"\nSimulation {y+1} of {nsim} simulation(s)\n")
        w = GenFreq(w0,N,m,h)

        pop = mod(N,nu)
        pop.generateX()

        k = 0
        while(pop.gene_count < NGI+1):
            pop.multiple_gene_model(h,pi,w)
            if k%int(N) == 0:   #every generation
                if k%int(w*N) == 0:
                    print(f"{pop.gene_count}-th gene   |  w = ",w)
                    w = GenFreq(w0,N,m,h)
                data.write(f"{pop.diversity(pop.X)},")
            k = k+1
        DeleteComma(data)
        data.write("\n")
    data.close()
    print(filename)

#simulations with multiple gene model. OUTPUT: Diversity per w
def DiversityMultipleGenePerFrequency(nsim,N,nu,h,m,g,pi,w0,NGI):


    global filename
    filename = f'max{nu}_{h}_{pi}_{N}_{w0}_{g}_{nsim}_multiple_gene_per_frequency+0'
    filename = ChangeName(filename)
    signal.signal(signal.SIGINT,sgn)

    data = open(filename,'w')
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
            w1 = w0/f
            w =GenFreq(w1,N,m,h)

            pop = mod(N,nu)
            pop.generateX()

            #Wait the diverisity is stabilized before to catch data
            for k in range(int(N/nu)):
                pop.neutral_model()
            pop.rename_species()
            pop.generateX()

            k = 0
            while(pop.gene_count < NGI+1):
                pop.multiple_gene_model(h,pi,w)
                if k%int(N) == 0:   #every generation
                    if k%int(w*N) == 0:
                        print(f"{pop.gene_count}-th gene   |  w = ",w)
                        w = GenFreq(w1,N,m,h)
                    S = S + pop.diversity(pop.X)
                    Ns = Ns+1;
                k = k+1
            data.write(f"{S/Ns/S0},")
            print(S/Ns/S0)
        DeleteComma(data)
        data.write("\n")
    data.close()
    print(filename)

#extract frequency values from exponential pdf
def GenFreq(w0,N,m,h):
    s = int(np.log(N)/(m+h))  #define very low w values threshore
    w = expon.rvs(loc=s, scale=w0, size=1)[0]
    while w == 0:   w = expon.rvs(loc=s, scale=w0, size=1)[0]

    return int(w)
