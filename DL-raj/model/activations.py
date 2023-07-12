import numpy as np

# activation functions and their derivative
# may contains utils function as well

def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2))

def mse_prime(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size
#------------------

def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1-np.tanh(x)**2
#------------------

def relu(x):
    return np.maximum(0, x)
def relu_prime(x):
    return np.where(x > 0, 1, 0)

#------------------

def mae(y_true, y_predicted):
    return np.abs(y_true-y_predicted)

def mae_prime(y_true, y_predicted):
    return np.sign(y_predicted-y_true)/y_true.size
#------------------
def linear(x):
    return x

def linear_prime(x):
    return np.ones_like(x)
#------------------

def r_squared(y_true, y_predicted):
    y_mean = np.sum(y_true)
    sstotal = np.sum((y_true-y_mean)**2)
    rss = np.sum((y_true-y_predicted)**2)

    r = 1-(rss/sstotal)
    return r
#------------------

def normalize(x):
    min_val = np.min(x)
    max_val = np.max(x)
    return (x-min_val)/(max_val-min_val)
#------------------

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))
#------------------

def softmax(x):
    e_x = np.exp(x-np.max(x))
    return e_x/np.sum(e_x)

def softmax_prime(x):
    return softmax(x)*(1-softmax(x))