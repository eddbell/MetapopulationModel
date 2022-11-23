import numpy as np, random, time
from numpy.random import rand, seed

class mod():
    def __init__(self,N,nu):
        self.N = N  #number of patches
        self.nu = nu    #innovation rate
        self.x = self.generatex()     #generate a meta-population without genes
        self.f = self.x               #define vector of genes
        self.X = self.generateX()     #generate one strain meta-population
        self.ngene = 0  #the numbers of genes in the meta-population of the last introducted gene.
        self.gene_count = 0     #numbers of differents genes

    #define the array containing the species.
    #The meta-population is initaliazed with all the patches having the same specie.
    def generatex(self):
        a = np.zeros(self.N,dtype = np.int64)
        return a

    #Join a new array to the previous, then attach to each species the presence or not of a gene
    def generateX(self):
        X = np.asarray([self.x,self.f])
        self.X = X
        return X

    #Neutral Model
    def neutral_model(self):
        h = np.random.uniform(0,1)
        if h >=self.nu:
            #migration
            s = np.random.randint(0,self.N)
            self.x = np.append(self.x[s],self.x)
            self.x = np.delete(self.x,np.random.randint(0,self.N))
        else:
            #innovation
            s = np.random.randint(0,self.N)
            self.x[s]= np.max(self.x)+1
        return 0

    #Model with the introduction of a single gene
    def gene_model(self,ph,pi,g):

        #define the distribution of gene in the innovations
        def distrgene(g):
            if 0<=g<=1:
                x = g
            else:
                u = np.random.uniform(0,1)
                g = self.ngene/self.N
                if u < g:
                    x = 1
                else:
                    x = 0
            return x
        pm = 1-pi-ph    #define migration rate

        #If there is not any gene in the meta-population, we introduce one in a random patch
        if self.ngene == 0:
            p1 = np.random.randint(self.N)
            self.X[1,p1] = 1
            self.ngene = self.ngene + 1

        #choose the position of 2 random patches
        p1 = np.random.randint(0,self.N)
        p2 = p1
        while p1==p2:
            p2 = np.random.randint(0,self.N)

        o = np.random.uniform(0,1)
        if o>self.nu:
            u = np.random.uniform(0,ph+pm+pi)
            if self.X[1,p1] == 0 and self.X[1,p2] == 1:
                if u<pm:    #CASE 1: Migration
                    self.X[:,p1] = self.X[:,p2]
                    self.ngene = self.ngene + 1
                elif u<pm+ph:   #CASE 2: Horizontal Gene Transfer
                    self.X[1,p1] = 1
                    self.ngene = self.ngene + 1
                elif u<1:   #CASE 3: patches that don't have the gene spread
                    self.X[:,p2] = self.X[:,p1]
                    self.ngene = self.ngene - 1
            elif self.X[1,p1] == 1 and self.X[1,p2] == 0:
                if u<pm:    #CASE 1: Migration
                    self.X[:,p2] = self.X[:,p1]
                    self.ngene = self.ngene + 1
                elif u<pm+pi:   #CASE 2: Horizontal Gene Transfer
                    self.X[:,p1] = self.X[:,p2]
                    self.ngene = self.ngene - 1
                elif u<1:   #CASE 3: spread of the patches that don't have the gene
                    self.X[1,p2] = 1
                    self.ngene = self.ngene + 1
            #if both the patches have the gene the next step is equal to the previous one
            elif self.X[1,p1] == 0 and self.X[1,p2] == 0:
                self.X[:,p2] = self.X[:,p1]
            #if both the patches don't have the gene the next step is equal to the previous one
            elif self.X[1,p1] == 1 and self.X[1,p2] == 1:
                self.X[:,p2] = self.X[:,p1]
        else:#innovation
            genesi = distrgene(g)
            self.ngene = self.ngene + genesi - self.X[1,p1]
            self.X[:,p1] = [max(self.X[0])+1,genesi]
        return 0

    #Model with the introduction of multiple gene with frequency w generation
    def multiple_gene_model(self,ph, pi,w,p,ngenerazioni,gene_count):
        N = self.N
        def distrgene():
            u = np.random.uniform(0,1)
            g = self.ngene/self.N
            if u < g:
                x = gene_count  #the innovation have a new gene
                ce = 1  #the innovation have the gene
            else:
                x = gene_count -1  #the innovation have an ancient gene
                ce = 0  #the innovation don't have the gene
            return x, ce
        pm = 1 - ph - pi

        #If there is not any gene in the meta-population, we introduce one in a random patch
        if self.ngene == 0:
            p1 = np.random.randint(0,N)
            self.X[1,p1] = gene_count
            self.ngene = self.ngene + 1

        #We choose 2 random patches
        p1 = np.random.randint(0,N)
        p2 = p1
        while p1==p2:
            p2 = np.random.randint(0,N)

        #Every w generation we introduce a new gene in a random patch
        #Because the w generation is N step long, we introduce the variable p which aims to introduce the gene just on the first step
        if ngenerazioni%w == 0 and p == 0:
            o = np.random.randint(0,N)
            gene_count = gene_count + 1
            self.X[1,o] = gene_count
            self.ngene = 1
            p = 1
        o = np.random.uniform(0,1)
        if o>self.nu:
            u = np.random.uniform(0,ph+pm+pi)
            if self.X[1,p1] != gene_count and self.X[1,p2] == gene_count:
                if u<pm:    #CASE 1: Migration
                    self.X[:,p1] = self.X[:,p2]
                    self.ngene = self.ngene + 1
                elif u<pm+ph:   #CASE 2: Horizontal Gene Transfer
                    self.X[1,p1] = gene_count
                    self.ngene = self.ngene + 1
                elif u<1:   #CASE 3: patches that don't have the gene spread
                    self.X[:,p2] = self.X[:,p1]
                    self.ngene = self.ngene - 1
            elif self.X[1,p1] == gene_count and self.X[1,p2] != gene_count:
                if u<pm:    #CASE 1: Migration
                    self.X[:,p2] = self.X[:,p1]
                    self.ngene = self.ngene + 1
                elif u<pm+pi:   #CASE 2: Horizontal Gene Transfer
                    self.X[:,p1] = self.X[:,p2]
                    self.ngene = self.ngene - 1
                elif u<1:   #CASE 3: patches that don't have the gene spread
                    self.X[1,p2] = gene_count
                    self.ngene = self.ngene + 1
            elif self.X[1,p1] == self.X[1,p2]:
                self.X[:,p1] = self.X[:,p2]
        else:#innovation
            genesi, ce = distrgene()
            if self.X[1,p1] == gene_count:
                cera = 1
            else:
                cera = 0
            self.ngene = self.ngene + ce - cera
            self.X[:,p1] = [max(self.X[0])+1,genesi]
        return p, ngenerazioni, gene_count

    #compute the diversity of the meta-population
    def diversity(self, arr):
        if np.shape(arr) == (2,self.N):
            s = len(np.unique(self.X[0]))
        else:
            s = len(np.unique(self.x))
        return s

    #remove the unused species labels from the array
    def rename_species(self):
        newname = 0
        for i in range(self.N):
            if self.x[i] >= self.N:
                for j in range(i+1,self.N):
                    if self.x[i] == self.x[j]:
                        self.x[j] = newname

                self.x[i]=newname
                newname = newname +1
        return 0
