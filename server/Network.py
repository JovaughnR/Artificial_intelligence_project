import numpy as np
import pickle

class Layer:
   def __init__(self, n_input, n_neuron, act=""):
      He = np.sqrt(2. / n_input)
      self.w = np.random.randn(n_input, n_neuron) * He
      self.b = np.random.randn(n_neuron)
      self.activation = act

   @staticmethod
   def softmax(x):
      # Compute the exponential of each element in the input vector
      exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
      return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
   
   @staticmethod
   def reLu(x):
      return np.maximum(0, x)  

   def forward(self, x:np.ndarray):
      self.input = x
      z = x.dot(self.w) + self.b

      if self.activation == "softmax":
         self.x = self.softmax(z)

      else:
         self.x = self.reLu(z)

      return self.x
   

class NeuralNetwork:
   def __init__(
         self, n_input, n_output, n_neuron, n_layers, 
         activation_in, activation_out
      ):
      if isinstance(n_neuron, tuple):
         n_neuron = n_neuron[0]

      self.size = n_layers
      self.layers = [None]*(self.size+1)

      # Construct the layers
      for i in range(self.size):
         self.layers[i] = Layer(n_input, n_neuron, activation_in)
         n_input = n_neuron

      # Output layer
      self.layers[-1] = Layer(n_input, n_output, activation_out)

   def softmax_derivative(self, output, y_true):
      # output is the softmax output, y_true is the one-hot encoded target vector
      return output - y_true
   
   def cross_entropy_loss(self, y_true, y_pred):
      y_pred = np.clip(y_pred, 1e-12, 1-1e-12)
      return -np.sum(y_true * np.log(y_pred))
   

   def reLu_derivative(self, y):
      return np.where(y > 0, 1, 0)
   
   def predict(self, X):
      for i in range(self.size+1):
         X = self.layers[i].forward(X)
      return Layer.softmax(X)
   
   def save(self, filepath):
      model_data = {
         "size":self.size,
         "layers": []
      }

      for layer in self.layers:
         model_data["layers"].append({
            "weights": layer.w,
            "biases": layer.b,
            "activation": layer.activation
         })
      
      with open(filepath, 'wb') as f:
         pickle.dump(model_data, f)

      print(f"Model saved to {filepath}")

   @staticmethod
   def load(filepath):
      with open(filepath, 'rb') as f:
         model_data = pickle.load(f)

      n_input = model_data["layers"][0]["weights"].shape[0]
      n_output = model_data["layers"][-1]["weights"].shape[1]
      n_layers = model_data["size"]
      n_neuron = model_data["layers"][0]["weights"].shape[1],  # assuming all hidden layers have the same neuron count
      activation_in = model_data["layers"][0]["activation"]
      activation_out = model_data["layers"][-1]["activation"]

      model = NeuralNetwork(
         n_input=n_input,
         n_output=n_output,
         n_neuron=n_neuron,
         n_layers=n_layers,
         activation_in=activation_in,
         activation_out=activation_out
      )
      
      for i, layer in enumerate(model_data["layers"]):
         model.layers[i].act = layer["activation"]
         model.layers[i].w = layer["weights"]
         model.layers[i].b = layer["biases"]

      print("Model loaded sucesfully")
      return model

   def train(
         self, X, y, batch_size=32, lr=0.001, epochs=1, epsilon=1e8
      ):

      n_samples = X.shape[0]
      initial_loss = 0

      # Training loop
      for epoch in range(epochs):
         # Forward propogation
         indices = np.random.permutation(n_samples)
         X_shuffled = X[indices]
         y_shuffled = y[indices]

         for i in range(0, n_samples, batch_size):
            x_batch = X_shuffled[i:i+batch_size]
            y_batch = y_shuffled[i:i+batch_size]

            output = x_batch
            for layer in self.layers:
               output = layer.forward(output)

            # Calculate the loss
            loss = self.cross_entropy_loss(y_batch, output)
            if initial_loss == 0:
               initial_loss = loss

            # Calcute the change in loss w.r.t (output)
            gradient = self.softmax_derivative(output, y_batch)

            # Back propogation from here
            for j in range(self.size, -1, -1):
               layer = self.layers[j]

               # Gradient for the weights
               grad_w = np.dot(layer.input.T, gradient)  # Matrix multiplication for weight gradient
               grad_b = np.sum(gradient, axis=0)

               # Update weights and biases
               layer.w -= lr * grad_w
               layer.b -= lr * grad_b

               # Calculate gradient for the previous layer 
               # (only apply ReLU derivative for hidden layers)# Calculate gradient for the previous layer
               if j > 0:
                  gradient = gradient.dot(layer.w.T)
                  gradient *= self.reLu_derivative(self.layers[j-1].x)

         print(f"Epochs {(epoch+1)/epochs*100:.2f} %, Loss: {(loss/initial_loss)*100:.2f}%")

      return self.layers
   
