import numpy as np

from model.network import Network
from model.fc_layer import FCLayer
from model.activation_layer import ActivationLayer
import model.activations as act
import matplotlib.pyplot as plt

# training data
x_train = np.array([[[0,0]], [[0,1]], [[1,0]], [[1,1]]])
y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

# network
net = Network()
net.add(FCLayer(2, 3))
net.add(ActivationLayer(act.tanh, act.tanh_prime))
net.add(FCLayer(3, 1))
net.add(ActivationLayer(act.tanh, act.tanh_prime))

# train
net.use(act.mse, act.mse_prime)

errors = net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

# test
out = net.predict(x_train)
print(out)
print(act.r_squared(y_train,out))
# # print(x_train.tolist()[0])
# x1_train = [i[0][0] for i in x_train.tolist()]
# x2_train = [i[0][1] for i in x_train.tolist()]

# z1 = [i[0][0] for i in y_train.tolist()]
# z2 = [i[0][0] for i in out]

# print(x1_train,x2_train,z1,z2)
# # #ploting error graph



# plt.scatter(z1,z2)
# plt.ylabel('Error')
# plt.xlabel('Epoch')

# plt.show()

# # from mpl_toolkits import mplot3d
# # import matplotlib.pyplot as plt
# # fig = plt.figure()
# # ax = fig.add_subplot(111, projection='3d')

# # # ax.plot3D(x1_train,x2_train,z1, label = 'dwae')

# # ax.plot(x1_train,x2_train,z2, label='predicted value')
# # ax.plot(x1_train,x2_train,z1,  label='real value')

# # ax.legend()
# # plt.show()