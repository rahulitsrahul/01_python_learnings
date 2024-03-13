import numpy as np
from matplotlib import pyplot as plt

alpha = (2* np.pi)/(200*16)
ft = 16e6 / 1
w_dot = 150


def get_cn(cn_prev, n):
    cn = cn_prev - ((2 * cn_prev)/((4*n) + 1))
    return round(cn)

c0 = 0.676 * ft * np.sqrt((2*alpha)/w_dot)
c0 = round(c0)
print(c0)
n = 0

cn_s = []
cn_s.append(c0)
cn_prev = c0

num_steps = 2000
for i in range(num_steps):
    n += 1
    
    cn_curr = get_cn(cn_prev, n)
    cn_s.append(cn_curr)
    
    cn_prev = cn_curr
    
plt.plot(cn_s)
plt.show()
    

