import sys
import numpy as np
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
k = int(sys.argv[1])
first_iteration = True

def isPrime(n):
    sw = True
    if(n < 2): return False
    j = 2
    while(j<=np.sqrt(n) and sw):
        if n % j == 0:
            sw = False
        j+=1
    return sw

num = 1
numofprimes=0
data = np.zeros(2,dtype=int)
numofproc = np.zeros(k,dtype=int)

t0 = time.time()
while num<=k:
    if rank==0:
        if first_iteration:
            for i in range(1,num_procs):
                if (num <= k):
                    data[0] = num
                    data[1] = num + 99
                    comm.send(data, dest=i)
                    num = data[1] + 1
            first_iteration=False
        res = comm.recv(source=MPI.ANY_SOURCE)
        numofproc[res[1]]+=1
        numofprimes+=res[0]
        if num<=k:
            data[0] = num
            data[1] = num + 99
            comm.send(data, dest=res[1])
            num = data[1] + 1
        else:
            comm.send([-1,-1], dest=res[1])
    else:
        cont = 0
        numRank = comm.recv(source=0)
        if numRank[0]!=-1:
            for i in range(numRank[0],numRank[1]):
                if(isPrime(i)):
                    cont+=1
            comm.send([cont,rank],dest=0)
tf = time.time()
if rank==0:
    print('El tiempo de ejecucion fue de: ',(tf-t0),'seg')
    print('El numero de primos es: ',numofprimes)
    print('Número de validaciones por proceso: ')
    for proc in range(1,num_procs):
        print('El proceso: ',proc,' Realizó: ',numofproc[proc],' Procesos' )
