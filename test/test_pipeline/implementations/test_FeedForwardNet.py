import unittest
import os
import numpy as np

from ParamSklearn.implementations.FeedForwardNet import FeedForwardNet

class TestFeedForwardNet(unittest.TestCase):
    def test_initial_feed_implementation(self):
        """
        Test initial implementation of NN Feed Forward architecture
        on Theano and Lasagne
        """

        # Simple test that hopefully works
        dataset_dir = '../data/'
        # Take training and data from binary classification
        X_train = np.load(dataset_dir + 'unit_train.npy')
        y_train = np.load(dataset_dir + 'unit_train_labels.npy')
        X_test = np.load(dataset_dir + 'unit_test.npy')
        y_test = np.load(dataset_dir + 'unit_test_labels.npy')

        # The input shape is using the batch size
        model = FeedForwardNet(input_shape=(50, 1, 1, 7), batch_size=50, num_epochs=2)
        # "Correct Shape"
        X_train = X_train[:, np.newaxis, np.newaxis, :]
        X_test = X_test[:, np.newaxis, np.newaxis, :]
        model.fit(X_train, y_train)
        print "Model fitted"

        predicted_probability_matrix = model.predict_proba(X_test)
        expected_labels = np.argmax(predicted_probability_matrix, axis=1)
        predicted_labels = model.predict(X_test)
        accuracy = np.count_nonzero(y_test == predicted_labels)
        print (float(accuracy) / float(X_test.shape[0]))

        self.assertTrue((predicted_labels == expected_labels).all(), msg="Failed predicted probability")
        self.assertTrue((1 - predicted_probability_matrix.sum(axis=1) < 1e-3).all())
