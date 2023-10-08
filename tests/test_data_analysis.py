import unittest
import numpy as np
from app.data_analysis import predict_distances


class TestDataAnalyis(unittest.TestCase):

    def test_predict_distances(self):
        test_data = np.load('test_data/test_features.npy')
        predicted = predict_distances(test_data)
        predicted = np.sort(predicted).astype(int)
        self.assertEqual(predicted[0], 300)
        self.assertEqual(predicted[1], 1000)
