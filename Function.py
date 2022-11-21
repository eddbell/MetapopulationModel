import numpy as np
from Model import mod
import os, signal, sys, csv

#Deletes the simulations file if you stop the process (CTRL+D)
def sgn(signal,frame):
    os.remove(filename)
    sys.exit(0)
signal.signal(signal.SIGINT,sgn)

#deletes the final comma in simulations
def DeleteComma(data):
    data.seek(0,2) # end of file
    size=data.tell() # the size...
    data.truncate(size-1)
    return 0

#simulation of neutral model. OUTPUT: diversity per generation
def DiversityNeutral(nsim,N,nu):
    print("------------------------------------\n")
    print("Execution neutral model")
    print("------------------------------------\n")
    filename = f'{N}_{nu}_{nsim}_neutral_model.csv'
    data = open(filename,'w')
    if nu != 0:  Nmax = int(3 * N / nu)
    for y in range(nsim):

        print(f"Innovation rate {nu} \nSimulation {y} of {nsim}\n")
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
    print("\n------------------------------------")
    print("Simulation of HGT & migration model.")
    print("------------------------------------\n")
    filename = f'0_{nu}_{h}_{pi}_{N}_{g}_diversity_gene.csv'
    data = open(filename,'w')

    if nu != 0:  Nmax = int(N / nu)
    for y in range(nsim):
        pop = mod(N,nu)
        print(f"Simulation {y}\n")
        print("Execution neutral model\n")
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
def DiversityMultipleGene(nsim,N,nu,h,m,g,pi,w,NGI):
    print("------------------------------------\n")
    print("Simulation of multiple gene model.")
    print("------------------------------------\n")
    
    p = 0   #triggered during the introduction of each gene.
    ngenerations = 0 #number of generations
    gene_count = 0  #numbers of differents genes
    
    w = int((2*np.log(N)/(h+m)+1/nu)/8)
    
    filename = f'0_{nu}_{h}_{pi}_{N}_{w}_{g}_trend_multiple_gene.csv'
    data = open(filename,'w')

    for y in range(nsim):
        print(f"Simulation {y+1} of {nsim} simulation(s)\n")
        pop = mod(N,nu)
        pop.generateX()
        for k in range(int(w*N*NGI)):
            p,ngenerations,gene_count = pop.multiple_gene_model(h, pi,w,p,ngenerations,gene_count)
            if k%int(N) == 0:
                ngenerations = ngenerations + 1
                if k%(w*N) == 0:
                    o = np.random.randint(0,N)
                    pop.gene_count = pop.gene_count + 1
                    pop.X[1,o] = pop.gene_count
                    pop.ngene = 1
                    print(pop.gene_count,"-th gene of ", NGI)
                data.write(f"{pop.diversity(pop.X)},")
                p=0
        DeleteComma(data)

        data.write("\n")
    data.close()
    print(filename)
    return 0
