import unittest

from autosklearn.pipeline.components.classification.adaboost import \
    AdaboostClassifier
from autosklearn.pipeline.util import _test_classifier, _test_classifier_predict_proba

import sklearn.metrics
import sklearn.ensemble
import numpy as np


class AdaBoostComponentTest(unittest.TestCase):
    def test_default_configuration_iris(self):
        for i in range(10):
            predictions, targets = \
                _test_classifier(AdaboostClassifier)
            self.assertAlmostEqual(0.93999999999999995,
                                   sklearn.metrics.accuracy_score(targets,
                                                                  predictions))

    def test_default_configuration_iris_predict_proba(self):
        for i in range(10):
            predictions, targets = \
                _test_classifier_predict_proba(AdaboostClassifier)
            self.assertAlmostEqual(0.34244204343758322,
                                   sklearn.metrics.log_loss(targets, predictions))

    def test_default_configuration_iris_sparse(self):
        for i in range(10):
            predictions, targets = \
                _test_classifier(AdaboostClassifier, sparse=True)
            self.assertAlmostEqual(0.88,
                                   sklearn.metrics.accuracy_score(targets,
                                                                  predictions))

    def test_default_configuration_multilabel(self):
        for i in range(10):
            predictions, targets = \
                _test_classifier(classifier=AdaboostClassifier,
                                 dataset='digits',
                                 make_multilabel=True)
            self.assertAlmostEqual(0.80933874118770355,
                                   sklearn.metrics.average_precision_score(
                                       targets, predictions))

    def test_default_configuration_multilabel_predict_proba(self):
        for i in range(10):
            predictions, targets = \
                _test_classifier_predict_proba(classifier=AdaboostClassifier,
                                 make_multilabel=True)
            self.assertEqual(predictions.shape, ((50, 3)))
            self.assertAlmostEqual(0.97856971820815897,
                                   sklearn.metrics.average_precision_score(
                                       targets, predictions))

    def test_default_configuration_binary(self):
        for i in range(10):
            predictions, targets = \
                _test_classifier(classifier=AdaboostClassifier,
                                 dataset='digits', sparse=True,
                                 make_binary=True)
            self.assertAlmostEqual(0.93199757134183359,
                                   sklearn.metrics.accuracy_score(
                                       targets, predictions))

    def test_target_algorithm_multioutput_multiclass_support(self):
        cls = sklearn.ensemble.AdaBoostClassifier()
        X = np.random.random((10, 10))
        y = np.random.randint(0, 1, size=(10, 10))
        self.assertRaisesRegexp(ValueError, 'bad input shape \(10, 10\)',
                                cls.fit, X, y)