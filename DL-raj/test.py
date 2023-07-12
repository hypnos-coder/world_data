import numpy as np

# Define the activation function (ReLU)
def relu(x):
    return np.maximum(0, x)

# Define the derivative of the activation function (ReLU)
def relu_derivative(x):
    return np.where(x > 0, 1, 0)

# Define the mean squared error loss function
def mse_loss(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Define the neural network class
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Initialize weights with random values
        self.W1 = np.random.randn(hidden_size, input_size)
        self.b1 = np.random.randn(hidden_size, 1)
        self.W2 = np.random.randn(output_size, hidden_size)
        self.b2 = np.random.randn(output_size, 1)

    def forward(self, X):
        # Forward propagation
        self.Z1 = np.dot(self.W1, X.T) + self.b1
        self.A1 = relu(self.Z1)
        self.Z2 = np.dot(self.W2, self.A1) + self.b2
        self.A2 = self.Z2  # Output layer uses a linear activation

    def backward(self, X, y):
        # Backpropagation
        m = X.shape[0]  # Number of training examples

        dZ2 = self.A2 - y.T
        dW2 = (1 / m) * np.dot(dZ2, self.A1.T)
        db2 = (1 / m) * np.sum(dZ2, axis=1, keepdims=True)
        dZ1 = np.dot(self.W2.T, dZ2) * relu_derivative(self.Z1)
        dW1 = (1 / m) * np.dot(dZ1, X)
        db1 = (1 / m) * np.sum(dZ1, axis=1, keepdims=True)

        return dW1, db1, dW2, db2

    def update_parameters(self, dW1, db1, dW2, db2, learning_rate):
        # Update weights and biases
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            self.forward(X)
            loss = mse_loss(y.T, self.A2)

            dW1, db1, dW2, db2 = self.backward(X, y)
            self.update_parameters(dW1, db1, dW2, db2, learning_rate)

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

        print(f"Final Loss: {loss}")

    def predict(self, X):
        self.forward(X)
        return self.A2.T

# Generate training data
np.random.seed(42)
X_train = np.random.randn(1000, 2)  # 1000 training examples, 2 input features
print(X_train)
y_train = X_train[:, 0]+ X_train[:, 1]  # Ground truth labels

# Create and train the neural network
input_size = 2
hidden_size = 3
output_size = 1
learning_rate = 0.1
epochs = 2000

model = NeuralNetwork(input_size, hidden_size, output_size)
model.train(X_train, y_train, epochs, learning_rate)

# Test the trained network on new data
X_test = np.array([[2, 2]])  # Single test example
prediction = model.predict(X_test)
print(f"Prediction: {prediction}")