
import numpy as np

# import resource
from HPOlibConfigSpace.configuration_space import ConfigurationSpace
from HPOlibConfigSpace.conditions import EqualsCondition, InCondition
from HPOlibConfigSpace.hyperparameters import UniformFloatHyperparameter, \
    UniformIntegerHyperparameter, CategoricalHyperparameter, \
    UnParametrizedHyperparameter

from autosklearn.pipeline.components.base import AutoSklearnClassificationAlgorithm
from autosklearn.pipeline.constants import *
from autosklearn.pipeline.implementations import FeedForwardNet


class Feed_NN(AutoSklearnClassificationAlgorithm):
    def __init__(self, number_epochs, batch_size, num_layers, num_units_layer_1,
                 num_units_layer_2, num_units_layer_3,num_units_layer_4,
                 num_units_layer_5, num_units_layer_6, dropout_layer_1,
                 dropout_layer_2, dropout_layer_3, dropout_layer_4,
                 dropout_layer_5, dropout_layer_6, dropout_output,
                 std_layer_1, std_layer_2, std_layer_3, std_layer_4,
                 std_layer_5, std_layer_6, learning_rate, solver,
                 momentum, beta1=0.9, beta2=0.9, rho=0.95, random_state=None):
        self.number_epochs = number_epochs
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.dropout_output = dropout_output
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.beta1 = beta1
        self.beta2 = beta2
        self.rho = rho
        self.solver = solver

        self.num_units_per_layer = []
        self.dropout_per_layer = []
        self.std_per_layer = []
        for i in range(1, num_layers):
            self.num_units_per_layer.append(int(eval("num_units_layer_" + str(i))))
            self.dropout_per_layer.append(float(eval("dropout_layer_" + str(i))))
            self.std_per_layer.append(float(eval("std_layer_" + str(i))))
        self.estimator = None

    # Basically the NN
    def fit(self, X, y):
        self.batch_size = int(self.batch_size)

        self.n_features = X.shape[1]
        self.input_shape = (self.batch_size, 1, 1, self.n_features)
        num_output_units = len(np.unique(y.astype(int)))

        # TODO: Ask Aaron about default shape
        X = X[:, np.newaxis, np.newaxis, :]

        #TODO: Create try-catch statement
        assert len(self.num_units_per_layer) == self.num_layers - 1
        assert len(self.dropout_per_layer) == self.num_layers - 1

        self.estimator = FeedForwardNet.FeedForwardNet(batch_size=self.batch_size,
                                                       input_shape=self.input_shape,
                                                       num_layers=self.num_layers,
                                                       num_units_per_layer=self.num_units_per_layer,
                                                       dropout_per_layer=self.dropout_per_layer,
                                                       std_per_layer=self.std_per_layer,
                                                       num_output_units=num_output_units,
                                                       dropout_output=self.dropout_output,
                                                       learning_rate=self.learning_rate,
                                                       momentum=self.momentum,
                                                       beta1=self.beta1,
                                                       beta2=self.beta2,
                                                       rho=self.rho,
                                                       solver=self.solver,
                                                       num_epochs=self.number_epochs)
        # TODO: Add number of epochs to space?
        self.estimator.fit(X, y)
        return self

    def predict(self, X):
        if self.estimator is None:
            raise NotImplementedError
        return self.estimator.predict(X)

    def predict_proba(self, X):
        if self.estimator is None:
            raise NotImplementedError()
        return self.estimator.predict_proba(X)

    @staticmethod
    def get_properties(dataset_properties=None):
        return {'shortname': 'feed_nn',
                'name': 'Feed Forward Neural Network',
                'handles_missing_values': False,
                'handles_nominal_values': False,
                'handles_numerical_features': True,
                'prefers_data_scaled': True,
                # TODO find out if this is good because of sparsity...
                'prefers_data_normalized': False,
                'handles_regression': False,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': False,
                'is_deterministic': True,
                'handles_sparse': False,
                'input': (DENSE, UNSIGNED_DATA),
                'output': (PREDICTIONS,),
                # TODO find out what is best used here!
                # C-continouos and double precision...
                'preferred_dtype': None}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None):

        solver_choices = ["adam", "adadelta", "adagrad", "sgd", "momentum", "nesterov"]

        layer_choices = [i for i in range(2, 7)]

        batch_size = UniformIntegerHyperparameter("batch_size", 100, 1000,
                                                  default=100)

        number_epochs = UniformIntegerHyperparameter("number_epochs", 2, 10,
                                                     default=3)

        num_layers = CategoricalHyperparameter("num_layers",
                                               choices=layer_choices,
                                               default=3)

        num_units_layer_1 = UniformIntegerHyperparameter("num_units_layer_1",
                                                         10, 6144,
                                                         default=10)

        num_units_layer_2 = UniformIntegerHyperparameter("num_units_layer_2",
                                                         10, 6144,
                                                         default=10)

        num_units_layer_3 = UniformIntegerHyperparameter("num_units_layer_3",
                                                         10, 6144,
                                                         default=10)

        num_units_layer_4 = UniformIntegerHyperparameter("num_units_layer_4",
                                                         10, 6144,
                                                         default=10)

        num_units_layer_5 = UniformIntegerHyperparameter("num_units_layer_5",
                                                         10, 6144,
                                                         default=10)

        num_units_layer_6 = UniformIntegerHyperparameter("num_units_layer_6",
                                                         10, 6144,
                                                         default=10)

        dropout_layer_1 = UniformFloatHyperparameter("dropout_layer_1",
                                                     0.0, 0.99, default=0.5)

        dropout_layer_2 = UniformFloatHyperparameter("dropout_layer_2",
                                                     0.0, 0.99, default=0.5)

        dropout_layer_3 = UniformFloatHyperparameter("dropout_layer_3",
                                                     0.0, 0.99, default=0.5)

        dropout_layer_4 = UniformFloatHyperparameter("dropout_layer_4",
                                                     0.0, 0.99, default=0.5)

        dropout_layer_5 = UniformFloatHyperparameter("dropout_layer_5",
                                                     0.0, 0.99, default=0.5)

        dropout_layer_6 = UniformFloatHyperparameter("dropout_layer_6",
                                                     0.0, 0.99, default=0.5)

        dropout_output = UniformFloatHyperparameter("dropout_output", 0.0, 0.99,
                                                    default=0.5)

        lr = UniformFloatHyperparameter("learning_rate", 1e-6, 1, log=True,
                                        default=0.01)

        momentum = UniformFloatHyperparameter("momentum", 0.3, 0.999,
                                              default=0.9)

        std_layer_1 = UniformFloatHyperparameter("std_layer_1", 1e-6, 0.1,
                                                 default=0.005)

        std_layer_2 = UniformFloatHyperparameter("std_layer_2", 1e-6, 0.1,
                                                 default=0.005)

        std_layer_3 = UniformFloatHyperparameter("std_layer_3", 1e-6, 0.1,
                                                 default=0.005)

        std_layer_4 = UniformFloatHyperparameter("std_layer_4", 1e-6, 0.1,
                                                 default=0.005)

        std_layer_5 = UniformFloatHyperparameter("std_layer_5", 1e-6, 0.1,
                                                 default=0.005)

        std_layer_6 = UniformFloatHyperparameter("std_layer_6", 1e-6, 0.1,
                                                 default=0.005)

        solver = CategoricalHyperparameter(name="solver",
                                           choices=solver_choices,
                                           default="sgd")

        beta1 = UniformFloatHyperparameter("beta1", 0.01, 1.0, default=0.9)
        beta2 = UniformFloatHyperparameter("beta2", 0.01, 1.0, default=0.9)
        rho = UniformFloatHyperparameter("rho", 0.0, 1.0, default=0.95)

        cs = ConfigurationSpace()
        cs.add_hyperparameter(number_epochs)
        cs.add_hyperparameter(batch_size)
        cs.add_hyperparameter(num_layers)
        cs.add_hyperparameter(num_units_layer_1)
        cs.add_hyperparameter(num_units_layer_2)
        cs.add_hyperparameter(num_units_layer_3)
        cs.add_hyperparameter(num_units_layer_4)
        cs.add_hyperparameter(num_units_layer_5)
        cs.add_hyperparameter(num_units_layer_6)
        cs.add_hyperparameter(dropout_layer_1)
        cs.add_hyperparameter(dropout_layer_2)
        cs.add_hyperparameter(dropout_layer_3)
        cs.add_hyperparameter(dropout_layer_4)
        cs.add_hyperparameter(dropout_layer_5)
        cs.add_hyperparameter(dropout_layer_6)
        cs.add_hyperparameter(dropout_output)
        cs.add_hyperparameter(std_layer_1)
        cs.add_hyperparameter(std_layer_2)
        cs.add_hyperparameter(std_layer_3)
        cs.add_hyperparameter(std_layer_4)
        cs.add_hyperparameter(std_layer_5)
        cs.add_hyperparameter(std_layer_6)
        cs.add_hyperparameter(lr)
        cs.add_hyperparameter(solver)
        cs.add_hyperparameter(momentum)
        cs.add_hyperparameter(beta1)
        cs.add_hyperparameter(beta2)
        cs.add_hyperparameter(rho)

        momentum_depends_on_solver = InCondition(momentum, solver, ["sgd", "momentum", "nesterov"])
        beta1_depends_on_solver = EqualsCondition(beta1, solver, "adam")
        beta2_depends_on_solver = EqualsCondition(beta2, solver, "adam")
        rho_depends_on_solver = EqualsCondition(rho, solver, "adadelta")
        cs.add_condition(beta1_depends_on_solver)
        cs.add_condition(beta2_depends_on_solver)
        cs.add_condition(rho_depends_on_solver)
        cs.add_condition(momentum_depends_on_solver)

        return cs
