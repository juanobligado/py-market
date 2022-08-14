import unittest

from agents.trading_agents import RandomTradingAgent
from exchange import OrderBook


class RandomAgentTestCase(unittest.TestCase):

    def test_should_generate_random_orders(self):
        order_book = OrderBook()
        agent1 = RandomTradingAgent(order_book, "Random Agent 1")
        agent1.on_price_tick(1,1.02)
        agent1.on_price_tick(1, 1.02)
        agent1.on_price_tick(1, 1.02)
        agent1.on_price_tick(1, 1.02)
        agent1.on_price_tick(1, 1.02)

        self.assertIsNot(0, order_book.get_buy_count())  # add assertion here
        self.assertIsNot(0, order_book.get_sell_count())

if __name__ == '__main__':
    unittest.main()
