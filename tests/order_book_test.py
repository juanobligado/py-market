import random
import unittest


from agents.trading_agents import RandomTradingAgent
from exchange import Order, OrderBook, OrderSide


class MyTestCase(unittest.TestCase):

    def test_match(self):
        book = OrderBook()
        agent = RandomTradingAgent(book,"Agent 1")
        agent_2 = RandomTradingAgent(book, "Agent 2")
        book.place_order(Order(agent,OrderSide.buy,1))
        book.place_order(Order(agent_2, OrderSide.sell, 1))
        book.match_trades(1,10.50)

        self.assertEqual(89.5, agent.portfoliomanager().get_usd_holding())
        self.assertEqual(101, agent.portfoliomanager().get_asset_holding())

        self.assertEqual(110.5, agent_2.portfoliomanager().get_usd_holding())
        self.assertEqual(99, agent_2.portfoliomanager().get_asset_holding())

    def test_match_should_pick_random(self):
        book = OrderBook()
        agent = RandomTradingAgent(book,"Agent 1")
        agent_2 = RandomTradingAgent(book, "Agent 2")
        agent_3 = RandomTradingAgent(book, "Agent 2")
        book.place_order(Order(agent,OrderSide.buy,1))
        book.place_order(Order(agent_2, OrderSide.sell, 1))
        book.place_order(Order(agent_3, OrderSide.sell, 1))
        # this seed makes next randrange(2) to return 1
        random.seed(2147483648)
        book.match_trades(1,10.50)
        self.assertEqual(110.5, agent_3.portfoliomanager().get_usd_holding())
        self.assertEqual(99, agent_3.portfoliomanager().get_asset_holding())

    def test_match_should_pick_random_2(self):
        book = OrderBook()
        agent = RandomTradingAgent(book,"Agent 1")
        agent_2 = RandomTradingAgent(book, "Agent 2")
        agent_3 = RandomTradingAgent(book, "Agent 2")
        book.place_order(Order(agent,OrderSide.buy,1))
        book.place_order(Order(agent_2, OrderSide.sell, 1))
        book.place_order(Order(agent_3, OrderSide.sell, 1))
        # this seed makes next randrange(2) to return 1
        random.seed(1)
        book.match_trades(1,10.50)
        self.assertEqual(110.5, agent_2.portfoliomanager().get_usd_holding())
        self.assertEqual(99, agent_2.portfoliomanager().get_asset_holding())


if __name__ == '__main__':
    unittest.main()
