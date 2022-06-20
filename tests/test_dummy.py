import unittest
import pytest


class TestSuite(unittest.TestCase):
    def setUp(self) -> None:
        # Do something
        pass

    @pytest.mark.smoke
    def test_1(self):
        self.assertTrue(1, 1)

    @pytest.mark.smoke
    def test_2(self):
        self.assertTrue(1, 1)

    @pytest.mark.regression
    def test_3(self):
        self.assertTrue(1, 1)

    @pytest.mark.regression
    def test_4(self):
        self.assertTrue(1, 1)

    @pytest.mark.regression
    def test_5(self):
        self.assertTrue(1, 1)

    def tearDown(self) -> None:
        # Do something
        pass


class TestSuite2(unittest.TestCase):
    def setUp(self) -> None:
        # Do something
        pass

    @pytest.mark.regression
    def test_11(self):
        self.assertTrue(1, 1)

    @pytest.mark.regression
    def test_12(self):
        self.assertTrue(1, 1)

    @pytest.mark.skip
    def test_13(self):
        # Under development
        pass

    @pytest.mark.skip
    def test_14(self):
        # Under development
        pass

    @pytest.mark.skip
    def test_15(self):
        # Under development
        pass

    def tearDown(self) -> None:
        # Do something
        pass


if __name__ == '__main__':
    unittest.main()
