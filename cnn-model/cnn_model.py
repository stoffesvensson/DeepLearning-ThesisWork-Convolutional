# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 11:48:22 2017

@author: Kristoffer
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

class CNN(object):
    
    def __init__(self, batch_size = 64):
        self.batch_size = batch_size
        self.number_of_classes = 2
        self.X_train = []
        self.X_test = []
        self.Y_train = []
        self.Y_test = []
        self.max_words = None
        self.vocabProcessor = None
        self.cnn_model = None
        self.model = None
        self.test_x = []
        self.test_y = []
        
        
    def load_dataset_training(self, vocab_name, filename = 'datasetWithoutNeutral'):
        """ Load the dataset """
        X, Y = load_csv('datasets/' + filename, target_column = 2, columns_to_ignore = [0])
        
        """ Count max words from the longest sentence """
        self.max_words = max([len(x[0].split(" ")) for x in X])
        
        """ Get vocabulare size from longest sentence """
        self.vocabProcessor = VocabularyProcessor(self.max_words)
        
        """ Encode pos, neu and neg to numbers """
        labelEncoder = LabelEncoder()
        labelEncoder.fit(Y)
        Y = labelEncoder.transform(Y)
        
        """ Change the list of sentences to a list of sequence of words """
        X = np.array(list(self.vocabProcessor.fit_transform([x[0] for x in X])))
        
        """ Split the datasets to training set and test test """
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size = 0.10, random_state = 7)
        
        """ Pad the sequences to fit the longest sentence """
        self.X_train = pad_sequences(self.X_train, maxlen = self.max_words, value=0.)
        self.X_test = pad_sequences(self.X_test, maxlen = self.max_words, value=0.)
        
        """ Convert labels to binary vector """
        self.Y_train = to_categorical(self.Y_train, nb_classes = self.number_of_classes)
        self.Y_test = to_categorical(self.Y_test, nb_classes = self.number_of_classes)
        self.vocabProcessor.save(vocab_name)
        
        
    def create_cnn_architecture_two_layers(self, model_name, outputDim = 300, number_of_filters = 60, filterSize = [3, 4],
                                           padding = 'same', activation_function_convLayer = 'relu', regularizer = 'L2',
                                           dropouts = 0.5, activation_function_fc = 'softmax', optimizer = 'adam',
                                           learning_rate = 0.001, loss_function = 'categorical_crossentropy'):
        if len(filterSize) == 0:
            filterSize = [3, 4]
        
        """ Define input shape and create word embedding """
        self.cnn_model = input_data(shape=[None, self.max_words], name='input')
        self.cnn_model = tflearn.embedding(self.cnn_model, input_dim = len(self.vocabProcessor.vocabulary_), output_dim = outputDim)
        
        """ Add three/two convolutional layer. Set number of filters and filter sizes and then merge together """
        conv1 = conv_1d(self.cnn_model, nb_filter = number_of_filters,  filter_size = filterSize[0], padding = padding,
                          activation = activation_function_convLayer, regularizer = regularizer)
        conv2 = conv_1d(self.cnn_model, nb_filter = number_of_filters,  filter_size = filterSize[1], padding = padding,
                          activation = activation_function_convLayer, regularizer = regularizer)
        #conv3 = conv_1d(cnn_model, nb_filter = 128,  filter_size = 5, padding = 'same',
         #                 activation = 'relu', regularizer = 'L2')
        self.cnn_model = merge([conv1, conv2], mode = 'concat', axis = 1)
        
        """ Expand one dimension to fit the max_pooling layer """
        self.cnn_model = tf.expand_dims(self.cnn_model, 1)
        self.cnn_model = global_max_pool(self.cnn_model)
        
        """ Instantiate dropout layer and specify dropout parameter """
        self.cnn_model = dropout(self.cnn_model, dropouts)
        
        """ Instantiate fully connected layer and regression layer. """
        self.cnn_model = fully_connected(self.cnn_model, self.number_of_classes, activation = activation_function_fc)
        self.cnn_model = regression(self.cnn_model, optimizer = optimizer, learning_rate = learning_rate, 
                           loss = loss_function, name = 'models/' + model_name)
        
        
    def train_and_save(self, model_name, tensorboard_verbose = 0, tensorboard_dir = '/logs/', nb_epochs = 5,
                       shuffle = True, show_metric = True):
        """ Instantiate Deep neural network model and start the training """
        self.model = tflearn.DNN(self.cnn_model, tensorboard_verbose = tensorboard_verbose, 
                            tensorboard_dir = tensorboard_dir)
        self.model.fit(self.X_train, self.Y_train, n_epoch = nb_epochs, validation_set = (self.X_test, self.Y_test), 
              shuffle = shuffle, show_metric = show_metric, batch_size = self.batch_size, run_id = model_name)
        
        """ Save the model """
        self.model.save('models/' + model_name)
        
        
    def load_model(self, model_name, outputDim = 300, number_of_filters = 60, filterSize = [3, 4],
                   padding = 'same', activation_function_convLayer = 'relu', regularizer = 'L2',
                   dropouts = 0.5, activation_function_fc = 'softmax', optimizer = 'adam',
                   learning_rate = 0.001, loss_function = 'categorical_crossentropy', 
                   tensorboard_verbose = 0, tensorboard_dir = '/logs/'):
        """
            Has to pass the same values that the models were trained with. If the
            model was trained on default values, the parameters will pass it automatically.
        """

        self.create_cnn_architecture_two_layers(model_name, outputDim, number_of_filters, filterSize,
                                                padding, activation_function_convLayer,
                                                regularizer, dropouts, activation_function_fc,
                                                optimizer, learning_rate, loss_function)
        
        self.model = tflearn.DNN(self.cnn_model, tensorboard_verbose = tensorboard_verbose,
                                 tensorboard_dir = tensorboard_dir)
        self.model.load('models/' + model_name)
        
        
    def load_test_dataset(self, filename = 'testDatasetWithOutNeuTwo', vocab_name = 'vocabProc'):
        """
            Something is wrong with this function. Does not get the same result
            as before when loading in the new data...
        """
        
        """ Load test dataset """
        self.test_x, self.test_y = load_csv('datasets/' + filename, target_column = 1)
        
        """ Get restored vocabulary processor """
        self.vocabProcessor = VocabularyProcessor(self.max_words)
        self.vocabProcessor.restore(vocab_name)
        
        """ Encode pos, neu and neg to numbers  """
        labelEncoder = LabelEncoder()
        labelEncoder.fit(self.test_y)
        self.test_y = labelEncoder.transform(self.test_y)
        
        """ Change the list of sentences to a list of sequence of words """
        self.test_x = np.array(list(self.vocabProcessor.transform([x[0] for x in self.test_x])))
        
        """ Pad the sequences to fit the longest sentence """
        self.test_x = pad_sequences(self.test_x, maxlen = self.max_words, value=0.)
        
        """ Convert labels to binary vector """
        self.test_y= to_categorical(self.test_y, nb_classes = self.number_of_classes)
        
        
    def evaluate_model_performance(self):
        metrix_score = self.model.evaluate(self.test_x, self.test_y, batch_size = self.batch_size)
        return metrix_score
        
        
    def predict_one_sentence(self, sentence = [['']], vocab_name = 'vocabProc'):
        """ Load vocabulary processor """
        self.vocabProcessor = VocabularyProcessor(self.max_words)
        self.vocabProcessor.restore(vocab_name)
        
        """ Transorm sentence to matrix of numbers """        
        sentence = np.array(list(self.vocabProcessor.transform([x[0] for x in sentence])))
        sentence = pad_sequences(sentence, max_len = self.vocabProcessor.max_document_length, value = 0.)
        
        """ Predict sentence """        
        pred_score = self.model.predict(sentence)
        return pred_score
        
        
    def predict_list(self, list_of_sentences = [[''], ['']], vocab_name = 'vocabProc'):
        """ Load vocabulary processor """
        self.vocabProcessor = VocabularyProcessor(self.max_words)
        self.vocabProcessor.restore(vocab_name)
        
        """ Transorm sentence to matrix of numbers """        
        sentence = np.array(list(self.vocabProcessor.transform([x[0] for x in sentece])))
        sentence = pad_sequences(sentence, max_len = self.vocabProcessor.max_document_length, value = 0.)
        
        """ Predict sentence """        
        pred_score = self.model.predict(list_of_sentences)
        return pred_score
        