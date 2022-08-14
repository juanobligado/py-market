import unittest

from indicators.indicator import *


class IndicatorTests(unittest.TestCase):
    def test_ma(self):
        n = 10
        ma = MovingAverage(n)
        size = ma.get_size()
        self.assertEqual(0,size)
        for i in range(0,10):
            ma.add_data_point(1.0)

        self.assertEqual(1,ma.get_value())
        ma.add_data_point(0.0)
        ma.add_data_point(0.0)
        self.assertEqual(0.8,ma.get_value())

    def test_price_position_constant_should_return_05(self):
        n = 10
        ma = TrailingPricePosition(4)
        size = ma.get_size()
        self.assertEqual(0,size)
        for i in range(0,4):
            ma.add_data_point(1.0)

        self.assertEqual(0.5,ma.get_value())



    def test_price_position_new_max_should_return_1(self):
        n = 10
        ma = TrailingPricePosition(4)
        size = ma.get_size()
        self.assertEqual(0,size)
        for i in range(0,4):
            ma.add_data_point(0.01 + 0.01*i)

        self.assertEqual(1.0,ma.get_value())

    def test_price_position_new_min_should_return_0(self):
        n = 10
        ma = TrailingPricePosition(4)
        size = ma.get_size()
        self.assertEqual(0,size)
        for i in range(0,4):
            ma.add_data_point(1.0 - 0.01*i)

        self.assertEqual(0.0,ma.get_value())
if __name__ == '__main__':
    unittest.main()
