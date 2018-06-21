import numpy
from numpy import linalg as lin

def newman_partiton(list, Adj):
    d = []
    for i in range(len(list)):
        row_sum = 0
        for j in range(len(list)):
                row_sum += Adj[j][i]

        d.append(row_sum)

    sum_D = numpy.sum(d)

    print(" > constructing the probability matrix ... ")

    P = numpy.empty(((len(list),len(list))))

    for i in range(len(list)):
        for j in range(len(list)):
            P[i][j] = (d[i] * d[j]) / sum_D


    M = numpy.subtract(Adj ,P)

    print(" > eigen-decomposition of modular matrix ... ")

    w, V = lin.eig(M)

    c1 = []
    c2 = []

    for i in range(len(list)):
        if(V[0][i] < 0):
            c1.append(list[i])
        else:
            c2.append(list[i])

    c1.sort()
    c2.sort()

    return c1 , c2
