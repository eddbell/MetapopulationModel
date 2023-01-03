# MetacommunityModel

Edoardo Bella 20 Nov 2022

Contents
========

 * [What is it?](#What)
 * [Configuration](#Configuration)
 * [Run](#Run)
 * [Plot](#Plot)

### What is it?

This GitHub repository contains the code for the simulation of sweeping beneficial genes in a meta-community of microorganisms. The model investigates the behaviour of biodiversity when a beneficial gene is spread.


### Configuration

The program is initialised with preset parameters. It is advisable to modify the parameters to manage the execution time of the programme.
The parameters required to execute the programme must be introduced during the execution of the code.
To display the parameters, simply run `$ python3 Main.py -h`


```shell
$ python3 Main.py -h

usage: Main.py [-h] [-N N] [-nu NU] [-ht HT] [-g G] [-pi PI] [-nsim NSIM]
               [-c COMMAND] [-w0 W0] [-NGI NGI]

Model simulations

optional arguments:
  -h, --help            show this help message and exit
  -N N                  Number of patches
  -nu NU                Innovation rate
  -ht HT                Horizontal gene transfer rate
  -g G                  Rate of the gene presence in the innovations, if g =
                        -1 probability = gene density in the meta-population
  -pi PI                Spread probability of patches without gene
  -nsim NSIM            Number of simulations
  -c COMMAND, --command COMMAND
                        Type of simulation
  -w0 W0                Frequency of genes introduction
  -NGI NGI              Number of introduced genes
```

### Run
To start the program, simply run `$ python3 Main.py` (if necessary defining the desired parameters) and then digit the number of the type of simulation you want to run:

```shell
$ python3 Main.py 
Namespace(N=10000, nu=0.01, ht=0.1, g=-1, pi=0, nsim=1, command=None, w=500)

Diversity per generation on Neutral Model  0

Diversity per generation on HGT & Migration Model  1

Diversity per generation on Multiple Gene Model  2


Please insert number of the model: 0

```


### Plot
It is possible to observe the numerical data of the simulation graphically by calling `$ ./ExecutePlot.py` and inserting the number of the file:

```shell
$ python3 ExecutePlot.py 
0_0.01_0.1_0_10000_20_-1_multiple_gene		 0
0_0.01_0.1_0_10000_500_-1_multiple_gene		 1
Insert number of the file : 1
```
The plot shows the diversity vs time of a single realization and the average over all realizations.



