import random
import numpy as np
a = np.zeros((5,5))
a[:,1] = np.random.randint(10,99,(1,5))
a[1,1] = 0
print(a)