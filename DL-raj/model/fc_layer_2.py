from model.layer import Layer
import numpy as np

# inherit from base class Layer
# implement the momentum optimization

class FCLayer(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weight = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        self.bias = np.zeros((1, output_size))
        
        self.momentum_weight = np.zeros_like(self.weight)
        self.momentum_bias = np.zeros_like(self.bias)
        self.velocity_weight = np.zeros_like(self.weight)
        self.velocity_bias = np.zeros_like(self.bias)
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weight) + self.bias
        return self.output

    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weight.T)
        weight_error = np.dot(self.input.T, output_error)
        bias_error = np.sum(output_error, axis=0, keepdims=True)

        self.momentum_weight = self.beta1 * self.momentum_weight + (1 - self.beta1) * weight_error
        self.momentum_bias = self.beta1 * self.momentum_bias + (1 - self.beta1) * bias_error
        self.velocity_weight = self.beta2 * self.velocity_weight + (1 - self.beta2) * (weight_error ** 2)
        self.velocity_bias = self.beta2 * self.velocity_bias + (1 - self.beta2) * (bias_error ** 2)

        m_weight_hat = self.momentum_weight / (1 - self.beta1)
        v_weight_hat = self.velocity_weight / (1 - self.beta2)
        m_bias_hat = self.momentum_bias / (1 - self.beta1)
        v_bias_hat = self.velocity_bias / (1 - self.beta2)

        self.weight -= (learning_rate * m_weight_hat) / (np.sqrt(v_weight_hat) + self.epsilon)
        self.bias -= (learning_rate * m_bias_hat) / (np.sqrt(v_bias_hat) + self.epsilon)

        return input_error