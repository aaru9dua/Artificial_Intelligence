# aarudua-a4
<h1>  k-nearest neighbors </h1>

<h2>Approach</h2>
1. Defined the euclidean and manhattan distances in util file.<br>
2. Setup the attribute in the class and ASSIGN THE data and target to the self parameters of the class for fitting.<br>
3. NOW LOOP THROUGH EACH POINTS IN TRAINING POINTS AND FIND THE DISTANCE BETWEEN TRAINPOINTS AND TESTING POINTS. <br>
4. NOW SORT THE DISTANCE AND PICK TO K neighbors and CHECK THE CATEGORIES OF THESE K POINTS IN SELF._Y LABEL. <br>
5. Based on the weight metric, If the weights are "uniform," then each point in each neighborhood is given the same weight. Closer neighbors of a train point will have a stronger effect than neighbors who are further away if the weights value is "distance." <br>
6. Finaly get the max label out of all the k neighbors, and append it in predict label. <br>

<h2> Accuracy </h2>
The accuracy report can be seen from the knn_iris_results.html and knn_digits_results.html and the accuracies coming out are really good.

<h2>Challenges</h2>
Understanding the distance metric, was a new challenge for me, otherwise everything was quite easy to implement.

<h1>  Multilayer Perceptron </h1>

<h2>Approach</h2>

1. Define all the Activation Function, loss function and one_hot_encoder in utils.py file-

>SIGMOID FUNCTION -

F(x)=1  / (1 + exp(-x))
And It’s derivative function will be - F(x) * (1 - F(x))

>TANH FUNCTION-

F(x)=(exp(x)-exp(-x))/(exp(x)+exp(-x))
And It’s derivative function will be -1-F(x)**2

>RELU FUNCTION-

F(x)=max(0,x)
And It’s derivative function will be - 1, if x>0 and 0 if x<=0

>CROSS ENTROPY

Loss= (- y * log(p))- ((1 - y) * log(1 - p))
<br>

2.SETUP THE ATTRIBUTES USING CLASS and do the one hot encoding of the label values

3. Depending on the kind of activation function, assign the weights and bias between the input to  hidden and  hidden to output layer. Identify or Sigmoid or TanH activation function works best with “xavier” initialization and Relu works best with "he" initialization and bias will be numbers between 0 to 1 and number of bias will depend upon size of hidden and output layers

4. Now start with training the neurons with forward propagation. Find the weighted sum by taking the dot product of the hidden layer weights and the input nodes and adding bias to it and Apply the activation function to the weighted sum. Now this value will use for the next layer. Find the weighted sum of next layer by taking the dot product of the updated values of hidden layers and the output nodes and adding bias to it and finally pass this weighted nodes through softmax activation function, because we want to class these nodes into categories

5. check the error by subtracting predicted y and actual y

6. Go through different iteration and update the weight and bias using Back Propagation that will produce least error. The weights between hidden  and output layer get updated by finding derivative of error with respect to the weights, update them using W1=W1-(learning_rate)*gradient_descent(error w.r.t W1) and gradient_descent(error w.r.t W1) (for a node in hidden layer) = [hidden_layer_values. error . f'(z) (derivative of output nodes)]/n and Update the bias by averaging the summation of the output_delta or input_delta.

7.Finally, Predict the labels of Test dataset, by Again feed forward the x_test points in the neural network and finding the maximum ouput values of each point.

<h2>Accuracy</h2>
The accuracy report can be seen from the mlp_iris_results.html and mlp_digits_results.html. Though the accuracy at very low learning rate is not very good.
<br>

<h2>Challenges</h2>
The problem faced during the training is that initially I was using random weight initializer but the accuracy was not really good and other than that during backpropagation, it was difficult to understant the how the exact input size should match with the derivate ones.
