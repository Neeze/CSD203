import random
import numpy as np
a = np.zeros((5,5))
dd = np.zeros((6,))
dd[1] = 1
print(dd)
a = []
for i in range(10):
    a.append(i)
print(a)
a.pop()
print(a)