#####https://wikidocs.net/14597

import numpy as np

a = np.array([1,2,3,4],)
b = np.array([5,6,7,8],)
print(a+b)
print(a*b)
print(a**2)
print(a+2)
print(10*np.sin(a))
print(a<3)

a *= b
print(a)

c = np.arange(9).reshape(3,3)
print(c)
print(c[:,1:])