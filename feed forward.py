import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Get input from the user for neural network architecture
num_hidden_layers = int(input("Enter the number of hidden layers: "))
hidden_layer_neurons = []

for i in range(num_hidden_layers):
    neurons = int(input(f"Enter the number of neurons in hidden layer {i + 1}: "))
    hidden_layer_neurons.append(neurons)

activation_function = input("Enter the activation function (e.g., 'relu', 'sigmoid'): ")

# Generate some dummy data for demonstration (you can replace this with your data)
X = np.random.rand(100, 10)
y = np.random.randint(2, size=(100,))

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a sequential model
model = tf.keras.Sequential()

# Add input layer
model.add(tf.keras.layers.Dense(hidden_layer_neurons[0], input_dim=X_train.shape[1], activation=activation_function))

# Add hidden layers
for neurons in hidden_layer_neurons[1:]:
    model.add(tf.keras.layers.Dense(neurons, activation=activation_function))

# Add output layer
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

