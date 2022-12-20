# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
#
# Submitted by: Aarushi Dua -- aarudua
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
import math
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding


class MultilayerPerceptron:
    """
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.

    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.

        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.

        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.

        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.

        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.

        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.

        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.

        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.

        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.

        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.

        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.

        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.

    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_hidden = 16, hidden_activation = 'sigmoid', n_iterations = 1000, learning_rate = 0.01):
        # Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
        activation_functions = {'identity': identity, 'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}

        # Check if the provided arguments are valid
        if not isinstance(n_hidden, int) \
                or hidden_activation not in activation_functions \
                or not isinstance(n_iterations, int) \
                or not isinstance(learning_rate, float):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the MultilayerPerceptron model object
        self.n_hidden = n_hidden
        self.hidden_activation = activation_functions[hidden_activation]
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self._output_activation = softmax
        self._loss_function = cross_entropy
        self._loss_history = []
        self._X = None
        self._y = None
        self._h_weights = None
        self._h_bias = None
        self._o_weights = None
        self._o_bias = None

    def _initialize(self, X, y):
        """
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        #Assign input to class variable
        self._X = X
        #Assign the one hot enocded version of output to class variable
        self._y = one_hot_encoding(y)


        np.random.seed(42)
        #https://machinelearningmastery.com/weight-initialization-for-deep-learning-neural-networks/
        #BASED ON THE ABOVE ARTICLE, Depending on the kind of activation function, there are different weight initialization strategies.
        #IN OUR CASE-
        #Identify or Sigmoid or TanH activation function works best with “xavier” initialization.
        #Relu works best with "he" initialization
       

        def xavier(input_size,output_size):
          #find a random weight from the uniform probability with lower value as -1/(n)^1/2 and upper value as 1/(n)^1/2
          l, u = -(1.0 / np.sqrt(input_size)), (1.0 / np.sqrt(input_size))
          init_weight= l + (np.random.random((input_size,output_size)) * (u - l))
          return init_weight


        def he_weight(input_size,output_size):

           #find a random weight from normal probability distribution that has a mean of 0 and a standard deviation of sqrt(2/n)
           std = np.sqrt(2.0 / input_size)
           init_weight = np.random.random((input_size,output_size)) * std
           return init_weight
        
        #FOR ACTIVATION FUNCTIONS OTHER THAN RELU
        if self.hidden_activation.__name__ in ['sigmoid', 'tanh','identify']:
          #pass the input size as shape of x and output size as hideen layer size for weights between input nodes and hidden nodes
          self._h_weights=xavier(len(self._X[0]),self.n_hidden)
          #bias will be numbers between 0 to 1 and randomly assigns number to bias for hideen layer nodes
          self._h_bias = np.random.random((1, self.n_hidden))

          
          #pass the input size as size of hidden nodes and output size as shape of output nodes for weights between hidden nodes and output nodes
          self._o_weights=xavier(self.n_hidden,len(self._y[0]))
          #bias will be numbers between 0 to 1 and randomly assigns number to bias for output layer nodes
          self._o_bias = np.random.random((1, len(self._y[0])))
        
        #FOR RELU ACTIVATION FUNCTIONS 
        else:

          self._h_weights=he_weight(len(self._X[0]),self.n_hidden)
          self._h_bias =np.random.random((1, self.n_hidden))

          self._o_weights=he_weight(self.n_hidden,len(self._y[0]))
          self._o_bias = np.random.random((1, len(self._y[0])))
        

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        #https://medium.com/@daniel.hellwig.p/mathematical-representation-of-a-perceptron-layer-with-example-in-tensorflow-754a38833b44
        self._initialize(X, y)
        
        #go through different iteration, to make update the weight and bias that will produce least errror
        for itr in range(self.n_iterations):

           #TRAIN THE neural NETWORK
           #forward propagation
           #Find the weighted sum by taking the dot product of the hidden layer weights and the input nodes and adding bias to it
           #Apply the activation function to the weighted sum
           Weighted_input = np.dot(self._X, self._h_weights) + self._h_bias
           activated_input= self.hidden_activation(Weighted_input)
            

           #Find the weighted sum of next layer by taking the dot product of the updated values of hidden layers and the output nodes and adding bias to it
           weighted_output= np.dot(activated_input,self._o_weights)+self._o_bias
           #finally pass this weighted nodes through softmax activation function, because we want to class these nodes into categories
           activated_output=self._output_activation(weighted_output)
           
           
           #NOW LET'S CHECK THE RESULT AND TRY TO DECREASE THE ERROR

           #Backward propagation

           #FIND THE ERROR BETWEEN GIVEN LABEL AND PREDICTED LABELS
           error = np.subtract(activated_output,self._y)
           
           #Update all weight between hidden and output layer

           #we need to find derivative of error with respect to the weights, update them using W1=W1-(learning_rate)*gradient_descent(error w.r.t W1)
           #gradient_descent(error w.r.t W1) (for a node in hidden layer) = [hidden_layer_values. error . f'(z) (derivative of output nodes)]/n
           derivative_output=self._output_activation(weighted_output, derivative=True)
           output_delta=error*derivative_output
           gradient_weight_output = (1/len(self._X)) * np.dot(output_delta.T, activated_input).T
           
           #Update the bias by averaging the summation of the output_delta
           gradient_bias_output = (1/len(self._X)) * np.sum(output_delta, axis = 0, keepdims = True)


           #updates weights between hidden and input layers
           #gradient_descent(input_error w.r.t W) (for a node in input layer) = [input_layer_values. input_error . f'(z) (derivative of hidden layer nodes)]/n
           derivated_input= self.hidden_activation(Weighted_input, derivative = True)
           #by chain_rule- input_delta will = output_weights*output_error*derivative_hidden_layer
           input_error=np.dot(self._o_weights, error.T).T
           input_delta= input_error*derivated_input
          

           gradient_weight_input = (1/len(self._X)) * np.dot(input_delta.T, self._X).T
           #Update the bias by averaging the summation of the input_delta
           gradient_bias_input = (1/len(self._X)) * np.sum(input_delta, axis = 0, keepdims = True)

           #UPDATES ALL THE WEIGHTS AND BIAS USING using W=W-(learning_rate)*gradient_descent(error w.r.t W)
           self._o_weights -= self.learning_rate * gradient_weight_output
           self._o_bias -= self.learning_rate * gradient_bias_output
           self._h_weights -= self.learning_rate * gradient_weight_input
           self._h_bias -= self.learning_rate * gradient_bias_input

           # Calculate the cross_entropy loss as it gives measures the performance of a classification model
           cross_entropy_loss = self._loss_function(self._y, activated_output)
           #After every 20 iterations, store the 
           if itr % 20 == 0:
              self._loss_history.append(cross_entropy_loss)



    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        
        predicted_label= []

        # LOOP THROUGH EACH POINT IN TEST_DATASET
        for X_test in X:
          
            
            # Again feed forward the x_test points in the neural network
            #from input to hidden
            weighted_test_input =  np.dot(X_test, self._h_weights) + self._h_bias
            
            activated_test_input = self.hidden_activation(weighted_test_input)
            
            #from hidden to output
            weighted_test_output = np.dot(activated_test_input, self._o_weights) + self._o_bias
            
            activated_test_output =  self._output_activation(weighted_test_output)

            # append the predicted the test label with maximum ouput values
            predicted_label.append(np.argmax(activated_test_output))
          
        return predicted_label
