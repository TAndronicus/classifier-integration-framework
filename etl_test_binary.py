import unittest

from etl import Etl
from etl_test_helper import EtlTestHelper


class EtlBinaryTest(unittest.TestCase):
    etl = Etl()
    etlHelper = EtlTestHelper()

    def test1(self):
        self.etlHelper.assert_matrices_equal(
            [
                [50, 50],
                [0, 0]
            ],
            self.etl.calculate_conf_matrix_binary(.5, 0, 100, 50)
        )

    def test2(self):
        self.etlHelper.assert_matrices_equal(
            [
                [50, 25],
                [25, 0]
            ],
            self.etl.calculate_conf_matrix_binary(.5, -1 / 3, 100, 75)
        )

    def test3(self):
        matrix_binary = self.etl.calculate_conf_matrix_binary(.6970, .385, 1650, 650)
        self.etl.print_conf_matrix(matrix_binary)
        self.etlHelper.assert_matrices_equal(
            [
                [450, 300],
                [200, 700]
            ],
            matrix_binary
        )

    def test4(self):
        self.etlHelper.assert_matrices_equal(
            [
                [50, 0],
                [50, 0]
            ],
            self.etl.calculate_conf_matrix_binary(.5, 0, 100, 100)
        )

    def test5(self):
        self.etlHelper.assert_matrices_equal(
            [
                [80, 20],
                [0, 0]
            ],
            self.etl.calculate_conf_matrix_binary(.8, 0, 100, 80)
        )

    def test6(self):
        self.etlHelper.assert_matrices_equal(
            [
                [80, 10],
                [10, 0]
            ],
            self.etl.calculate_conf_matrix_binary(.8, -1 / 9, 100, 90)
        )

    def test7(self):
        self.etlHelper.assert_matrices_equal(
            [
                [80, 0],
                [0, 20]
            ],
            self.etl.calculate_conf_matrix_binary(1, 1, 100, 80)
        )

    def test8(self):
        self.etlHelper.assert_matrices_equal(
            [
                [0, 70],
                [30, 0]
            ],
            self.etl.calculate_conf_matrix_binary(0, -1, 100, 30)
        )

    def test9(self):
        self.etlHelper.assert_matrices_equal(
            [
                [100, 0],
                [0, 0]
            ],
            self.etl.calculate_conf_matrix_binary(1, 0, 100, 100)
        )

    def test10(self):
        self.etlHelper.assert_matrices_equal(
            [
                [0, 0],
                [100, 0]
            ],
            self.etl.calculate_conf_matrix_binary(0, 0, 100, 100)
        )

    def test11(self):
        self.etlHelper.assert_matrices_equal(
            [
                [23, 17],
                [13, 19]
            ],
            self.etl.calculate_conf_matrix_binary(.5833, 0.1677, 72, 36)
        )

    def test12(self):
        self.etlHelper.assert_matrices_equal(
            [
                [97, 1],
                [2, 0]
            ],
            self.etl.calculate_conf_matrix_binary(.97, -0.0144, 100, 99)
        )

    def test13(self):
        matrix = self.etl.calculate_conf_matrix_binary(.97, 0.6556, 100, 96)
        self.etl.print_conf_matrix(matrix)
        self.etlHelper.assert_matrices_equal(
            [
                [94, 1],
                [2, 3]
            ],
            matrix
        )

    def test14(self):
        matrix_binary = self.etl.calculate_conf_matrix_binary(.6970, .385, 16500, 6500)
        self.etl.print_conf_matrix(matrix_binary)
        self.etlHelper.assert_matrices_equal(
            [
                [4500, 3000],
                [2000, 7000]
            ],
            matrix_binary
        )


if __name__ == '__main__':
    unittest.main()
