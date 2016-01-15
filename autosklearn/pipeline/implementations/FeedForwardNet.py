"""
Created on Jul 22, 2015
Modified on Dec 3, 2015

@author: Aaron Klein
@modified: Hector Mendoza
"""
DEBUG = True

import numpy as np
import theano
import theano.tensor as T
import lasagne


def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


class FeedForwardNet(object):
    def __init__(self, input_shape=(100, 1, 1, 28*28),
                 batch_size=100, num_layers=2, num_units_per_layer=[10, 10],
                 dropout_per_layer=[0.5, 0.5], std_per_layer=[0.005, 0.005],
                 num_output_units=2, dropout_output=0.5, learning_rate=0.01,
                 momentum=0.9, beta1=0.9, beta2=0.999,
                 rho=0.95, solver="sgd", num_epochs=3):

        # I don't like the idea that parameters have
        # a default with random values
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.num_layers = num_layers
        self.num_units_per_layer = num_units_per_layer
        self.dropout_per_layer = dropout_per_layer
        self.num_output_units = num_output_units
        self.dropout_output = dropout_output
        self.std_per_layer = std_per_layer
        self.momentum = momentum
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.rho = rho
        self.num_epochs = num_epochs

        # TODO: Add correct theano shape constructor - Currently 4-tuple
        input_var = T.tensor4('inputs')
        target_var = T.ivector('targets')
        if DEBUG:
            print("... building network")
            print input_shape

        self.network = lasagne.layers.InputLayer(shape=input_shape,
                                                 input_var=input_var)
        # Define each layer
        for i in range(num_layers - 1):
            self.network = lasagne.layers.DenseLayer(
                 lasagne.layers.dropout(self.network,
                                        p=self.dropout_per_layer[i]),
                 num_units=self.num_units_per_layer[i],
                 W=lasagne.init.Normal(std=self.std_per_layer[i], mean=0),
                 b=lasagne.init.Constant(val=0.0),
                 nonlinearity=lasagne.nonlinearities.rectify)

        # Define output layer
        self.network = lasagne.layers.DenseLayer(
                 lasagne.layers.dropout(self.network, p=self.dropout_output),
                 num_units=self.num_output_units,
                 W=lasagne.init.GlorotNormal(),
                 b=lasagne.init.Constant(),
                 nonlinearity=lasagne.nonlinearities.softmax)

        prediction = lasagne.layers.get_output(self.network)
        loss = lasagne.objectives.categorical_crossentropy(prediction,
                                                           target_var)
        # Aggregate loss mean function
        loss = loss.mean()
        params = lasagne.layers.get_all_params(self.network, trainable=True)

        if solver == "nesterov":
            updates = lasagne.updates.nesterov_momentum(loss, params,
                                                        learning_rate=self.learning_rate,
                                                        momentum=self.momentum)
        elif solver == "adam":
            updates = lasagne.updates.adam(loss, params,
                                           learning_rate=self.learning_rate,
                                           beta1=self.beta1, beta2=self.beta2)
        elif solver == "adadelta":
            updates = lasagne.updates.adadelta(loss, params,
                                               learning_rate=self.learning_rate,
                                               rho=self.rho)
        elif solver == "adagrad":
            updates = lasagne.updates.adagrad(loss, params,
                                              learning_rate=self.learning_rate)
        elif solver == "sgd":
            updates = lasagne.updates.sgd(loss, params,
                                         learning_rate=self.learning_rate)
        elif solver == "momentum":
            updates = lasagne.updates.momentum(loss, params,
                                               learning_rate=self.learning_rate,
                                               momentum=self.momentum)
        else:
            updates = lasagne.updates.sgd(loss, params,
                                          learning_rate=self.learning_rate)

        # valid_prediction = lasagne.layers.get_output(self.network,
                                                     # deterministic=True)

        # valid_loss = lasagne.objectives.categorical_crossentropy(
                                                        # valid_prediction,
                                                        # target_var)
        # valid_loss = valid_loss.mean()
        # valid_acc = T.mean(T.eq(T.argmax(valid_prediction, axis=1),
                                # target_var),
                                # dtype=theano.config.floatX)

        print("... compiling theano functions")
        self.train_fn = theano.function([input_var, target_var], loss,
                                        updates=updates,
                                        allow_input_downcast=True)

        # Not so sure about this thing
        # self.test_fn = theano.function([input_var, target_var],
                                      # [valid_loss, valid_acc],
                                      # allow_input_downcast=True)

    def fit(self, X, y):
        for epoch in range(self.num_epochs):
            # TODO: Add exception RaiseError in shape
            train_err = 0
            train_batches = 0
            # if DEBUG:
            #   start_time = time.time()
            for batch in iterate_minibatches(X, y, self.batch_size, shuffle=True):
                inputs, targets = batch
                train_err += self.train_fn(inputs, targets)
                train_batches += 1
            # learning_curve[epoch] = (val_acc / float(val_batches) * 100)
        return self

    def predict(self, X):
        pred = self.predict_proba(X)
        return np.argmax(pred, axis=1)

    def predict_proba(self, X):
        predictions = lasagne.layers.get_output(self.network, X, deterministic=True).eval()
        return predictions
