import numpy as np


from model.network import Network
from model.fc_layer_2 import FCLayer
from model.activation_layer import ActivationLayer
import pandas as pd
import model.activations as act
import matplotlib.pyplot as plt

df = pd.read_csv("data/USA_Housing.csv")
# df
features =df[[ 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                'Area Population']]
target = df[['Price']]
# target

def generate_combination(df):# modify data presentation to suit the model
    result = []
    for _, row in df.iterrows():
        combination = list(row)
        result+=[[combination]]

    # split the data into training data(60%) and test data(40%)
    test_length = round(0.4*len(result))
    train_length = len(result)-test_length

    train_data = result[0:train_length]
    test_data = result[train_length:]
    return np.array(train_data), np.array(test_data)

x_train,x_test = generate_combination(features)
y_train,y_test = generate_combination(target)


# print(len(x_test))
# x_train
# neural network building

net = Network()


net.add(FCLayer(3, 8))
net.add(ActivationLayer(act.linear, act.linear_prime))
net.add(FCLayer(8, 6))
net.add(ActivationLayer(act.linear, act.linear_prime))
net.add(FCLayer(6, 1))
net.add(ActivationLayer(act.linear, act.linear_prime))


net.use(act.mse, act.mse_prime)

errors = net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

# test
out = net.predict(x_test)

# r_2 = act.r_squared(y_train,out)
# print(out)
# print(r_2)

# sns.displot((y_train-out),bins=50); 

plt.scatter(y_test,out)
plt.ylabel('out')
plt.xlabel('y_test')

plt.show()

