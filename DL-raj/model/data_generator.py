# used to generate data for model testing.

import numpy as np
np.random.seed(42)

def f(x,y,z,p):
    eq='2*x**2+y**2+z**3-p**4+2'
    x=str(x)
    y=str(y)
    z=str(z)
    p=str(p)
    eq=eq.replace('x',str(x),1)
    eq=eq.replace('y',str(y),1)
    eq=eq.replace('z',str(z),1)
    eq=eq.replace('p',str(p),1)
    return eval(eq)

def data_generator(m):
    x_list = [np.random.randn() for i in range(m)]
    y_list = [np.random.randn() for i in range(m)]
    z_list = [np.random.randn() for i in range(m)]
    p_list = [np.random.randn() for i in range(m)]

    data = []
    output = []
    for x,y,z,p in zip(x_list,y_list,z_list,p_list):
        data+=[[[x,y,z,p]]]
        output+=[[[f(x,y,z,p)]]]

    return np.array(data), np.array(output)

# print(data_generator(3))

