# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by:Aarushi Dua -- aarudua
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        #ASSIGN THE data and target to the self parameters of the class for fitting
        self._X = X
        self._y = y

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        #INITIALIZE TO STORE LABEL AFTER EACH PREDICTION
        predict_labels=[]
        for test_feature in X:
          
          #WILL LOOP THROUGH EACH POINTS IN TRAINING POINTS AND FIND THE DISTANCE BETWEEN TRAINPOINTS AND TESTING POINTS
          distance=[]
          for train_feature in self._X:

            distance.append(self._distance(train_feature,test_feature))
            
           
          #NOW SORT THE DISTANCE AND PICK TO K neighbors 
          k_nearest_points=np.argsort(distance)[:self.n_neighbors]
          
          
          k_label=[]
          
        #NOW CHECK THE CATEGORIES OF THESE K POINTS IN SELF._Y LABEL
          max_group={}
          for point in k_nearest_points:
            k_label.append(self._y[point])
          #REFRENCE-https://vitalflux.com/k-nearest-neighbors-explained-with-python-examples/#:~:text=If%20the%20value%20of%20weights,neighbors%20which%20are%20further%20away.
          #ABOVE LINK HELPED TO UNDERSTAND THE DIFFERENCE BETWEEN UNIFORM AND DISTANCE METRIC
          #If the weights are "uniform," then each point in each neighborhood is given the same weight. Closer neighbors of a train point will have a stronger effect than neighbors who are further away if the weights value is "distance."
          for i in range(len(k_nearest_points)):
              if self.weights =='uniform':
                   
                  if k_label[i] not in max_group:
                    max_group[k_label[i]]=0
                  #count the maximum category in k-points by counting labels
                  max_group[k_label[i]]+=1

              elif self.weights =='distance':
                if k_label[i] not in max_group:
                    max_group[k_label[i]]=0
                
                #the chance of the label is inversely proportion to the distance between points
                if k_label[0]==0:
                    max_group[k_label[i]]+=1
                else:
                  max_group[k_label[i]]+=1/k_label[0]
          
        
          #finaly get the max label out of all the keys, and append it in predict label
          max_value_label=max(max_group, key = max_group.get)
          predict_labels.append(max_value_label)  
        
        return  predict_labels
