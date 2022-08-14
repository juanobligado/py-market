import random

from exchange import *
from indicators.indicator import MovingAverage, TrailingPricePosition


class RandomTradingAgent(TradingAgent):

    def __init__(self, order_book: OrderBook, name: str):
        super().__init__(order_book, name)

    def before_simulation(self) -> None:
        pass

    def on_price_tick(self, t, price) -> None:
        sides = [OrderSide.buy, OrderSide.sell]
        side = random.choice(sides)
        order = Order(self, side, 1)
        self.order_book.place_order(order)

    def after_simulation(self) -> None:
        pass


class MomentumTradingAgent(TradingAgent):

    def __init__(self, order_book: OrderBook, name: str, short_period: int, long_period: int):
        super().__init__(order_book, name)
        self.ma_long = MovingAverage(long_period)
        self.ma_short = MovingAverage(short_period)
        self.last_order = OrderSide.none

    def before_simulation(self) -> None:
        pass

    def on_price_tick(self, t, price) -> None:
        # dont do anything on warmup period
        self.ma_short.add_data_point(price)
        self.ma_long.add_data_point(price)
        signal = self.signal()
        if signal != self.last_order:
            order = Order(self, signal, 1)
            self.order_book.place_order(order)
            self.last_order = signal

    def signal(self) -> OrderSide:
        if self.ma_long.is_ready() and self.ma_short.is_ready():
            last_ma_short = self.ma_short.get_value()
            last_ma_long = self.ma_long.get_value()
            if last_ma_short > last_ma_long:
                return OrderSide.buy
            if last_ma_short < last_ma_long:
                return OrderSide.sell

        return OrderSide.none

    def after_simulation(self) -> None:
        pass


class MeanRevertTradingAgent(TradingAgent):

    def __init__(self, order_book: OrderBook, name: str, period: int):
        self.order_book = order_book
        self.portfolio = PortfolioManager()
        self.name = name
        self.price_position = TrailingPricePosition(period)
        self.last_order = OrderSide.none
        self.buy_threshold = 0.25
        self.sell_threshold = 0.75

    def before_simulation(self) -> None:
        pass

    def on_price_tick(self, t, price) -> None:
        # dont do anything on warmup period
        self.price_position.add_data_point(price)

        signal = self.signal()
        if signal != self.last_order:
            order = Order(self, signal, 1)
            self.order_book.place_order(order)
            self.last_order = signal

    def signal(self) -> OrderSide:
        if self.price_position.is_ready():
            price_position = self.price_position.get_value()
            if price_position > self.sell_threshold:
                return OrderSide.sell
            elif price_position < self.buy_threshold:
                return OrderSide.buy

        return OrderSide.none

    def after_simulation(self) -> None:
        pass
