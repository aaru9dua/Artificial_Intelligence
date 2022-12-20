# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
#
# Submitted by: Aarushi Dua -- aarudua
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np


def euclidean_distance(x1, x2):
    """
    Computes and returns the Euclidean distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """

    #d = √[(x2 – x1)2 + (y2 – y1)2]
    #inbuilt library in numpy
    e_distance = np.linalg.norm(x1 - x2)
    return e_distance


def manhattan_distance(x1, x2):
    """
    Computes and returns the Manhattan distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    #Σ|Xi – Yi|
    m_distance=sum(abs(num1-num2) for num1, num2 in zip(x1,x2))

    return m_distance


def identity(x, derivative = False):
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    #F(X)=X
    #F'(X)=1
    if derivative:
      return 1

    else:
      return x




def sigmoid(x, derivative = False):
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """

    y= 1. / (1. + np.exp(-x))
    if derivative:
      #TAKE THE DERIVATIVE OF ABOVE SIGMOID VALUE Y
        return y * (1 - y)
    return y


def tanh(x, derivative = False):
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """

    y=(np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
    if derivative==True:
      y=1-y**2
      return y
    else:
      return y


def relu(x, derivative = False):
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
  
    
    if derivative:
      return 1* (x > 0)
    else:
      return x * (x > 0)



def softmax(x, derivative = False):
    x = np.clip(x, -1e100, 1e100)
    if not derivative:
        c = np.max(x, axis = 1, keepdims = True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis = 1, keepdims = True)))
    else:
        return softmax(x) * (1 - softmax(x))


def cross_entropy(y, p):
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.

    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the softmax
            output activation function.
    """


    entropy=(- y * np.log(p))- ((1 - y) * np.log(1 - p))
    return entropy


def one_hot_encoding(y):
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.

    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """
    
    y=np.array(y)
    y1=np.zeros((y.size, y.max() + 1))
    y1[np.arange(y.size), y] = 1

    return y1
