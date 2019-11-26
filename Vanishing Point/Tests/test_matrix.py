from unittest import TestCase

from Kalman_Filter import matrix


class TestMatrix(TestCase):

    def setUp(self):
        self.matrix = matrix([[10000., 0.], [0., 10000.]])

    def test_zero(self):
        self.zero = self.matrix.zero(5, 10)
        self.assertEqual(self.zero, -2)

    def test_identity(self):
        self.identity = self.matrix.identity(500)
        self.assertEqual(self.identity, -10)

    # def test_show(self):
    #     self.fail()
    #
    # def test_transpose(self):
    #     self.fail()
    #
    # def test_Cholesky(self):
    #     self.fail()
    #
    # def test_CholeskyInverse(self):
    #     self.fail()
    #
    # def test_inverse(self):
    #     self.fail()
