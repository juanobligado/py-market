import unittest

from agents.trading_agents import MomentumTradingAgent
from exchange import OrderBook, OrderSide


class MomentumAgentTest(unittest.TestCase):
    def test_momentum_signal(self):

        order_book = OrderBook()
        agent = MomentumTradingAgent(order_book,"",1,2)
        agent.on_price_tick(0, 10.0)
        # Should generate nothing
        self.assertEqual(OrderSide.none,agent.signal())
        # initializers warmed up should have If Momentum continues dont send new orders
        agent.on_price_tick(0, 15.0)
        self.assertEqual(OrderSide.buy, agent.signal())
        self.assertEqual(1,order_book.get_buy_count())

    def test_should_not_send_new_order_on_same_signal(self):
        order_book = OrderBook()
        agent = MomentumTradingAgent(order_book,"",1,2)
        agent.on_price_tick(0, 10.0)
        agent.on_price_tick(0, 15.0)
        agent.on_price_tick(0, 20.0)
        self.assertEqual(OrderSide.buy, agent.signal())
        self.assertEqual(1,order_book.get_buy_count())

    def test_should_not_send_new_order_on_same_signal_short(self):
        order_book = OrderBook()
        agent = MomentumTradingAgent(order_book,"",1,2)
        agent.on_price_tick(0, 10.0)
        agent.on_price_tick(0, 7.0)
        agent.on_price_tick(0, 5.0)
        self.assertEqual(OrderSide.sell, agent.signal())
        self.assertEqual(1,order_book.get_sell_count())

if __name__ == '__main__':
    unittest.main()
