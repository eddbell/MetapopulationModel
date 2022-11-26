#!/usr/bin/env python3
import numpy as np, time
import argparse

from Function import DiversityNeutral, DiversityGene, DiversityMultipleGene

t0 = time.time()
N = 10_000  #numbers of patches
nu = 0.01   #innovation rate
g = -1  # Rate of the gene presence in the innovations, if g = -1 probability = gene density in the meta-population
nsim = 1    #number of simulations
h = 0.1 #probability Horizontal Gene Transfer
pi = 0  #Spread probability of patches without gene
m = 1-(h+pi)    #migration probability
w = int((2*np.log(N)/(h+m)+1/nu))     #frequencies of gene introduction (in number of generations)
NGI = 4     #Number of genes introduced
command = 0     #number of the function called in Function.py

parser = argparse.ArgumentParser(description="Model simulations")
parser.add_argument("-N",help="Number of patches",type=int)
parser.add_argument("-nu",help="Innovation rate",type=float)
parser.add_argument("-ht",help="Horizontal gene transfer rate",type=float)
parser.add_argument("-g",help="Rate of the gene presence in the innovations, if g = -1 probability = gene density in the meta-population",type=float)
parser.add_argument("-pi",help="Spread probability of patches without gene",type=float)
parser.add_argument("-nsim",help="Number of simulations",type=int)
parser.add_argument("-w",help="Frequency of genes introduction")
parser.add_argument("-NGI",help="Number of genes introduced")
parser.add_argument("-c","--command",help="Type of simulation")
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

if args.w != None: w=int(args.w)
else:   args.w = w

if args.NGI != None: NGI=int(args.NGI)
else:   args.NGI = NGI

if args.command != None: command=args.command

if args.g != None:
    g=args.g
else: args.g = g


if command == 0:
    print("\nDiversity per generation on Neutral Model  1\n\nDiversity per generation on HGT & Migration Model  2\n\nDiversity per generation on Multiple Gene Model  3\n\n")
    command = input("Please insert number of the model: \n\n")

print(f"PARAMETERS:\nN {N}, h {h},g {g},pi {pi}, w {w}, nu {nu}, nsim {nsim}, NGI {NGI}\n")


#simulations of a meta-population WITHOUT introduction of a gene. OUTPUT: Diversity per generation
if  int(command) == 1:
    DiversityNeutral(nsim,N,nu)

#simulations of a meta-population WITH introduction of a gene. OUTPUT: Diversity per generation
elif int(command) == 2:
    DiversityGene(nsim,N,nu,h,m,g,pi)

#simulations with multiple gene model. OUTPUT: Diversity per generation
elif int(command) == 3:
    DiversityMultipleGene(nsim,N,nu,h,m,g,pi,w,NGI)


#print time of execution
print("execution time = ",time.time()-t0)
