import numpy as np

from model.network import Network
from model.fc_layer import FCLayer
from model.activation_layer import ActivationLayer
import model.activations as act

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def f(x):
    return x*x

def generate(m):
    x_list = [np.random.randint(-50,50) for i in range(100)]
    output = []
    data = []
    for x in x_list:
        data+=[x]
        output+=[f(x)]

    return act.normalize(np.array(data)), act.normalize( np.array(output))

# training data
x_train,y_train = generate(500)
x_test,y_test = generate(100)

# print(x_train)

# network
net = Network()
net.add(FCLayer(1, 10))
net.add(ActivationLayer(act.tanh, act.tanh_prime))
net.add(FCLayer(10, 1))
net.add(ActivationLayer(act.tanh, act.tanh_prime))

# train
net.use(act.mse, act.mse)

errors = net.fit(x_train, y_train, epochs=1000, learning_rate=0.01)

# test
out = net.predict(x_test)

r_2 = act.r_squared(out, y_test)
# print(out)
print(r_2)

plt.scatter(x_test,out)
plt.scatter(x_test,y_test)
plt.ylabel('out')
plt.xlabel('y_test')

plt.show()
#####

# plt.plot(list(range(400)),errors)
# plt.ylabel('error')
# plt.xlabel('epoch')

# plt.show()
