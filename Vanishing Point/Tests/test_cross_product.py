from unittest import TestCase

import numpy as np

from intersection_library import cross_product


class TestCross_product(TestCase):
    def test_cross_product(self):
        self.cross_product = cross_product(np.array([5, 3, 1]), np.array([4, 2, 1]))
        self.assertEquals(self.cross_product[0][0], 1)
        self.assertEquals(self.cross_product[0][1], -1)
        self.assertEquals(self.cross_product[0][2], -2)
