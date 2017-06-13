# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:03:17 2017

@author: Kristoffer

    This is a playground file to test how TFlearn and its functionality
    works. The models made with the script is working, the file itself just
    needs some cleaning
    
"""

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
import tflearn
import tensorflow as tf
from tflearn.data_utils import VocabularyProcessor
from tflearn.data_utils import pad_sequences, to_categorical, load_csv
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_1d, global_max_pool, max_pool_1d
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression

batch_size = 64
""" Load the dataset """
#X, Y = load_csv('datasetFullList', target_column = 2, columns_to_ignore = [0])
X, Y = load_csv('datasetWithoutNeutral', target_column = 2, columns_to_ignore = [0])

""" Count max words from the longest sentence """
max_words = max([len(x[0].split(" ")) for x in X])

""" Get vocabulare size from longest sentence """
vocab = VocabularyProcessor(max_words)

""" Encode pos, neu and neg to numbers """
labelEncoder = LabelEncoder()
labelEncoder.fit(Y)
Y = labelEncoder.transform(Y)

""" Change the list of sentences to a list of sequence of words """
X = np.array(list(vocab.fit_transform([x[0] for x in X])))

""" Split the datasets to training set and test test """
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.10, random_state = 7)

""" Pad the sequences to fit the longest sentence """
X_train = pad_sequences(X_train, maxlen = max_words, value=0.)
X_test = pad_sequences(X_test, maxlen = max_words, value=0.)

""" Convert labels to binary vector """
Y_train = to_categorical(Y_train, nb_classes = 2)
Y_test = to_categorical(Y_test, nb_classes = 2)
vocab.save('vocabProc')


""" 
    Begin the creation of convolutional model
"""

""" Define input shape and create word embedding """
cnn_model = input_data(shape=[None, max_words], name='input')
cnn_model = tflearn.embedding(cnn_model, input_dim = len(vocab.vocabulary_), output_dim = 300)

""" Add three/two convolutional layer. Set number of filters and filter sizes and then merge together """
conv1 = conv_1d(cnn_model, nb_filter = 60,  filter_size = 3, padding = 'same',
                  activation = 'relu', regularizer = 'L2')
conv2 = conv_1d(cnn_model, nb_filter = 60,  filter_size = 4, padding = 'same',
                  activation = 'relu', regularizer = 'L2')
#conv3 = conv_1d(cnn_model, nb_filter = 128,  filter_size = 5, padding = 'same',
 #                 activation = 'relu', regularizer = 'L2')
cnn_model = merge([conv1, conv2], mode = 'concat', axis = 1)

""" Expand one dimension to fit the max_pooling layer """
cnn_model = tf.expand_dims(cnn_model, 1)
cnn_model = global_max_pool(cnn_model)

""" Instantiate dropout layer and specify dropout parameter """
cnn_model = dropout(cnn_model, 0.8)

""" Instantiate fully connected layer and regression layer. """
cnn_model = fully_connected(cnn_model, 2, activation = 'softmax')
cnn_model = regression(cnn_model, optimizer = 'adam', learning_rate = 0.001, 
                       loss = 'categorical_crossentropy', name = 'target')
    
    
""" Instantiate Deep neural network model and start the training """
model = tflearn.DNN(cnn_model, tensorboard_verbose = 0, tensorboard_dir = '/logs/')
model.fit(X_train, Y_train, n_epoch = 5, validation_set = (X_test, Y_test), 
          shuffle = True, show_metric = True, batch_size = batch_size, run_id = 'NewArchitectureTest1')

""" Save the model """
model.save('cnn-newArchitecture3convs')

    
"""
    Load dataset and load the model for evaluation
"""

tf.reset_default_graph()

""" Load the dataset """
#test_x, test_y = load_csv('testDatasetWithNeuOne', target_column = 1)
#test_x, test_y = load_csv('testDatasetWithNeuTwo', target_column = 1)
#test_x, test_y = load_csv('testDatasetWithOutNeuOne', target_column = 1)
test_x, test_y = load_csv('testDatasetWithOutNeuTwo', target_column = 1)

""" Count max words from the longest sentence """
#max_words = max([len(x[0].split(" ")) for x in test_x])
max_words = 2132

""" Get vocabulare size from longest sentence """
vocab = VocabularyProcessor(max_words)
vocab = vocab.restore('vocabProc')

""" Encode pos, neu and neg to numbers """
labelEncoder = LabelEncoder()
labelEncoder.fit(test_y)
test_y = labelEncoder.transform(test_y)

""" Change the list of sentences to a list of sequence of words """
test_x = np.array(list(vocab.transform([x[0] for x in test_x])))

""" Pad the sequences to fit the longest sentence """
test_x = pad_sequences(test_x, maxlen = max_words, value=0.)

""" Convert labels to binary vector """
test_y= to_categorical(test_y, nb_classes = 2)
#test_y= to_categorical(test_y, nb_classes = 3)

""" Create the same neural network as the one that is going to be loaded. """
cnn_model = input_data(shape=[None, max_words], name='input')
cnn_model = tflearn.embedding(cnn_model, input_dim = len(vocab.vocabulary_), output_dim = 300)

""" Add three/two convolutional layer. Set number of filters and filter sizes and then merge together """
conv1 = conv_1d(cnn_model, nb_filter = 60,  filter_size = 3, padding = 'same',
                  activation = 'relu', regularizer = 'L2')
conv2 = conv_1d(cnn_model, nb_filter = 60,  filter_size = 4, padding = 'same',
                  activation = 'relu', regularizer = 'L2')
#conv3 = conv_1d(cnn_model, nb_filter = 128,  filter_size = 5, padding = 'same',
 #                 activation = 'relu', regularizer = 'L2')
cnn_model = merge([conv1, conv2], mode = 'concat', axis = 1)

""" Expand one dimension to fit the max_pooling layer """
cnn_model = tf.expand_dims(cnn_model, 1)
cnn_model = global_max_pool(cnn_model)

""" Instantiate dropout layer and specify dropout parameter """
cnn_model = dropout(cnn_model, 0.8)

""" Instantiate fully connected layer and regression layer. """
cnn_model = fully_connected(cnn_model, 3, activation = 'softmax')
cnn_model = regression(cnn_model, optimizer = 'adam', learning_rate = 0.001, 
                       loss = 'categorical_crossentropy', name = 'target')

""" Instantiate Deep neural network model and start the training """
model = tflearn.DNN(cnn_model, tensorboard_verbose = 0, tensorboard_dir = '/logs/')

""" Load models """
model.load('./cnn17')


"""
    Evaluate model performance and predict a score 
"""
        

""" Evaluate the models performance """
metrix_score = model.evaluate(test_x, test_y, batch_size = batch_size)

""" Predict 10 reviews """
pred_score = model.predict(test_x)


"""
    Test to predict own strings
"""
validate = [['Restaurangens mat var så pass dålig att jag spydde'], ['Älskar den servicen som de ger'], ['vet ej vad jag skall säga, inget dåligt inget bra']]
validate_x = np.array(list(vocab.transform([x[0] for x in validate])))
validate_x = pad_sequences(validate_x, maxlen = max_words, value = 0.)
result = model.predict(validate_x) 
