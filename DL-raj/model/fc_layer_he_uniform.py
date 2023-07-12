from model.layer import Layer
import numpy as np

# inherit from base class Layer
# fully connected layer, compute the math
class FCLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, input_size, output_size):
        
        self.weights = np.random.uniform(low=-np.sqrt(6/input_size), high=np.sqrt(6/input_size),size=(input_size,output_size))
        self.bias = np.random.rand(1, output_size)

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)
        bias_error = np.sum(output_error,axis=0,keepdims=True)
        # dBias = output_error

        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * bias_error
        return input_error