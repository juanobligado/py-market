import unittest
from runner.runner import Simulator
from timeseries.random_walk import RandomWalk
from agents.trading_agents import RandomTradingAgent
from exchange import OrderBook
from typing import List


class MyTestCase(unittest.TestCase):
    def test_simulation(self):

        order_book = OrderBook()
        agent1 = RandomTradingAgent(order_book, "Random Agent 1")
        agent2 = RandomTradingAgent(order_book, "Random Agent 2")
        agents = [agent1,agent2]

        time_series = RandomWalk.generate(1000)
        simulator = Simulator(agents, time_series,order_book)
        simulator.run()


if __name__ == '__main__':
    unittest.main()
