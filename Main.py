#!/usr/bin/env python3
import numpy as np, time
import argparse

from Function import DiversityNeutral, DiversityGene, DiversityMultipleGene, DiversityMultipleGenePerFrequency

t0 = time.time()
N = 10_000  #numbers of patches
nu = 0.01   #innovation rate
g = -1  # Rate of the gene presence in the innovations, if g = -1 probability = gene density in the meta-population
nsim = 1    #number of simulations
h = 0.1 #probability Horizontal Gene Transfer
pi = 0  #Spread probability of patches that don't have the gene
m = 1-(h+pi)    #migration probability
w0 = int((2*np.log(N)/(h+m)+1/nu))     #frequencies of gene introduction (in number of generations)
command = 0     #number of the function called in Function.py

parser = argparse.ArgumentParser(description="Model simulations")
parser.add_argument("-N",help="Number of patches",type=int)
parser.add_argument("-nu",help="Innovation rate",type=float)
parser.add_argument("-ht",help="Horizontal gene transfer rate",type=float)
parser.add_argument("-g",help="Rate of the gene presence in the innovations, if g = -1 probability = gene density in the meta-population",type=float)
parser.add_argument("-pi",help="Spread probability of patches without gene",type=float)
parser.add_argument("-nsim",help="Number of simulations",type=int)
parser.add_argument("-c","--command",help="Type of simulation")
parser.add_argument("-w0",help="Frequency of genes introduction")
args = parser.parse_args()

if args.N != None:  N=args.N
else:   args.N = N

if args.nu != None: nu=args.nu
else:   args.nu = nu

if args.ht != None: h=args.ht
else:   args.ht = h

if args.pi != None: pi=args.pi
else:   args.pi = pi

if args.nsim != None: nsim=args.nsim
else:   args.nsim = nsim

if args.w0 != None: w0=int(w0/float(args.w0))
else:   args.w0 = w0

if args.command != None: command=args.command

if args.g != None:
    g=args.g
else: args.g = g


if command == 0:
    print("\nDiversity per generation on Neutral Model  1\n\nDiversity per generation on HGT & Migration Model  2\n\nDiversity per generation on Multiple Gene Model  3\n\nDiversity per generation on Multiple Gene Model per frequency  4\n\n")
    command = input("Please insert number of the model: \n\n")


print("\n##################################################################################################\n")


#simulations of a meta-population WITHOUT introduction of a gene. OUTPUT: Diversity per generation
if  int(command) == 1:
    DiversityNeutral(nsim,N,nu)
    print("Execution neutral model.    OUTPUT: Diversity (S) per generations.")

#simulations of a meta-population WITH introduction of a gene. OUTPUT: Diversity per generation
elif int(command) == 2:
    DiversityGene(nsim,N,nu,h,m,g,pi)
    print("Simulation of HGT & migration model.    OUTPUT: Diversity (S) per generations.")

#simulations with multiple gene model. OUTPUT: Diversity per generation
elif int(command) == 3:
    DiversityMultipleGene(nsim,N,nu,h,m,g,pi,w0)
    print("Simulation of multiple gene model.    OUTPUT: Diversity (S) per generations.")

#simulations with multiple gene model. OUTPUT: Diversity per generation
elif int(command) == 4:
    DiversityMultipleGenePerFrequency(nsim,N,nu,h,m,g,pi,w0)
    print("Simulation of multiple gene model.    OUTPUT: mean diversity (S) over neutral diversity (S0) per w.")


print(f"PARAMETERS:\nN {N}, h {h},g {g},pi {pi}, w0 {w0}, nu {nu}, nsim {nsim}\n")

print("\n##################################################################################################\n")

#print time of execution
print("execution time = ",time.time()-t0)
