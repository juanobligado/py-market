import random
from abc import ABCMeta, abstractmethod
from enum import Enum


class OrderSide(Enum):
    none = -1
    buy = 0
    sell = 1


class Order:
    __metaclass__ = ABCMeta

    def __init__(self, agent, side: OrderSide, q: int):
        self.order_side = side
        self.order_quantity = q
        self.order_owner = agent

    def side(self) -> OrderSide:
        return self.order_side

    def quantity(self) -> int:
        return self.order_quantity

    def notify_fill(self, q: int, price: float):
        self.order_owner.on_trade_execution(self, q, price)


class PortfolioManager:

    def __init__(self):
        self.usdHolding = 100.0
        self.assetHolding = 100.0

    def get_usd_holding(self):
        return self.usdHolding

    def get_asset_holding(self):
        return self.assetHolding

    def trade_asset_usd(self, size: int, price: float):
        self.usdHolding = self.usdHolding - size * price
        self.assetHolding = self.assetHolding + size

    def print_summary(self, t, s, name):
        print(f"[time: {t} - {name}] - Asset Holdings {self.assetHolding}, USD Holdings: {self.usdHolding}]")


class OrderBook:

    def __init__(self):
        # Since we always buy / sell at market there is no need to handle price levels yet
        from exchange import Order
        self.buys = []
        self.sells = []

    def get_buy_count(self):
        return len(self.buys)

    def get_sell_count(self):
        return len(self.sells)

    def place_order(self, order: Order) -> bool:
        if order.quantity() == 0:
            print(f"Ignoring Order since size is 0")
            return False

        if order.side() == OrderSide.buy:
            self.buys.append(order)

        if order.side() == OrderSide.sell:
            self.sells.append(order)

        return

    def match_trades(self, t: int, market_price: float) -> None:
        # We can do this because order
        while self.get_buy_count() > 0 and self.get_sell_count() > 0:
            buy_index = 0
            sell_index = 0

            if len(self.buys) > 1:
                buy_index = random.randrange(len(self.buys))
            if len(self.sells) > 1:
                sell_index = random.randrange(len(self.sells))

            buy = self.buys.pop(buy_index)
            sell = self.sells.pop(sell_index)
            trade = Trade(buy, sell, 1, market_price)
            trade.notify()

        # orders ara all fill or kill
        self.reset()
        return

    def reset(self):
        self.buys.clear()
        self.sells.clear()


class TradingAgent:
    __metaclass__ = ABCMeta

    def __init__(self, order_book: OrderBook, name: str):
        self.order_book = order_book
        self.portfolio = PortfolioManager()
        self.name = name

    def portfoliomanager(self):
        return self.portfolio

    @abstractmethod
    def before_simulation(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_price_tick(self, t, price) -> None:
        raise NotImplementedError

    def after_price_tick(self, t, price) -> None:
        if t % 100 == 0:
            self.portfolio.print_summary(t, price, self.name)

    @abstractmethod
    def after_simulation(self) -> None:
        raise NotImplementedError

    def on_trade_execution(self, order: Order, fill_quantity: int, fill_price: float) -> None:
        fill = fill_quantity
        side = "Buy"
        if order.side() == OrderSide.sell:
            fill = -fill_quantity
            side = "Sell"

        self.portfolio.trade_asset_usd(fill, fill_price)

        # print(f"[{self.name}] {side} {fill_quantity} at {fill_price}")


class Trade:
    def __init__(self, buy: Order, sell: Order, fill: int, price: float):
        self.buy = buy
        self.sell = sell
        self.fill = fill
        self.price = price

    def notify(self):
        self.buy.notify_fill(self.fill, self.price)
        self.sell.notify_fill(self.fill, self.price)
