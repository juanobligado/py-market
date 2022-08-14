from typing import List
import matplotlib.pyplot as plt;
import numpy

from agents.trading_agents import TradingAgent
from exchange import OrderBook


class ReportGenerator:

    def __init__(self):
        self.report_map = {}

    def add_point(self, portfolio: str, field_name: str, value: float):
        key = f"{portfolio}:{field_name}"
        if key in self.report_map:
            self.report_map[key].append(value)
        else:
            a = [value]
            self.report_map[key] = a

    def plot(self):

        for k, values in self.report_map.items():
            [portfolio, field_name] = k.split(':')
            index = range(0, len(values))
            plt.plot(index, values, label=f"{portfolio}_{field_name}")
        plt.legend(loc="upper right")
        plt.show()


class Simulator:
    def __init__(self, agents: List[TradingAgent], price: numpy.array(float), book: OrderBook):
        self.agents = agents
        self.prices = price
        self.order_book = book
        self.report_generator = ReportGenerator()

    def run(self):
        # Initialize agents before running simulation
        for agent in self.agents:
            agent.before_simulation()

        for timestep in range(0, len(self.prices)):
            price = self.prices[timestep]

            # raise price tick so agents can send orders
            for agent in self.agents:
                agent.on_price_tick(timestep, price)

            # Run Order Book Matching Cycle
            self.order_book.match_trades(timestep, price)

            # raise price tick so agents can send orders
            for agent in self.agents:
                agent.after_price_tick(timestep, price)
                self.report_generator.add_point(agent.name, "usd", agent.portfoliomanager().get_usd_holding())
                self.report_generator.add_point(agent.name, "asset", agent.portfoliomanager().get_asset_holding())

        for agent in self.agents:
            agent.after_simulation()

        self.report_generator.plot()
