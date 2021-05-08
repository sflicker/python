import numpy as np
import random

def doubles(maxk, maxn):
    # make k and n numpy arrays
    k = np.arange(1, maxk+1, dtype=np.float64)
    n = np.arange(1, maxn+1, dtype=np.float64)
    # turn n into a column vector
    n = n[:, np.newaxis]
    return np.sum(1.0/np.multiply(k, np.power(n+1, 2*k)))


print(1, 10, doubles(1, 10))
print(10, 1000, doubles(10, 1000))
print(10, 10000, doubles(10, 10000))
print(10, 20000, doubles(20, 20000))
for i in range(100):
    k = random.randrange(10, 100)
    n = random.randrange(10000, 30000)
    print(k, n, doubles(k, n))

