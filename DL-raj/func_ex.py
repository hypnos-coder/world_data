import numpy as np

from model.network import Network
from model.fc_layer_2 import FCLayer
from model.activation_layer import ActivationLayer
import model.activations as act
import matplotlib.pyplot as plt
from model.data_generator import data_generator
import matplotlib.pyplot as plt

# training data
x_train,y_train = data_generator(1000)
# testing data
x_test,y_test = data_generator(500)

# print(x_train)

# network
net = Network()
net.add(FCLayer(4, 8))
net.add(ActivationLayer(act.linear, act.linear_prime))
net.add(FCLayer(8, 6))
net.add(ActivationLayer(act.linear, act.linear_prime))
net.add(FCLayer(6, 10))
net.add(ActivationLayer(act.linear, act.linear_prime))
net.add(FCLayer(10, 1))
net.add(ActivationLayer(act.linear, act.linear_prime))

# train
net.use(act.mae, act.mae_prime)

errors = net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

# test
out = net.predict(x_test)

r_2 = act.r_squared(y_test,out)
# print(out)
print(r_2)

plt.scatter(y_test,out)
plt.ylabel('out')
plt.xlabel('y_test')

plt.show()
#####

# plt.plot(list(range(400)),errors)
# plt.ylabel('error')
# plt.xlabel('epoch')

# plt.show()
