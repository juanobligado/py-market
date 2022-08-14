import unittest
from timeseries import random_walk


class MyTestCase(unittest.TestCase):
    def test_randomwalk(self):
        x = randomwalk.RandomWalk.generate(1000)
        self.assertEqual(1, x[0])
        size = len(x)
        for i in range(1, len(x)):
            v = x[i]
            if v == 0:
                continue

            if x[i - 1] != 0:
                r = x[i] / x[i - 1] - 1.0
                self.assertLessEqual(abs(r), 1.0, "Return should be between -1% and 1%")


if __name__ == '__main__':
    unittest.main()
