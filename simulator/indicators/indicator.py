import numpy as np
from abc import ABCMeta, abstractmethod


class Indicator:
    __metaclass__ = ABCMeta

    def __init__(self, n: int):
        self.buffer = None
        self.is_warm_up = False
        self.n = n

    def get_size(self) -> int:
        if self.buffer is None:
            return 0
        shape = self.buffer.size
        return shape

    def add_data_point(self, p: float):
        new_array = np.array([p])
        if self.is_warm_up:
            self.buffer = np.concatenate((self.buffer[1:], new_array))
        else:
            if self.buffer is None:
                self.buffer = new_array
            else:
                self.buffer = np.concatenate((self.buffer, new_array))
            if self.get_size() == self.n:
                self.is_warm_up = True

    def is_ready(self):
        return self.is_warm_up

    @abstractmethod
    def get_value(self) -> float:
        pass


class MovingAverage(Indicator):
    def __init__(self, n: int):
        self.buffer = None
        self.is_warm_up = False
        self.n = n

    def get_value(self):
        return self.buffer.mean()


class TrailingPricePosition(Indicator):
    def __init__(self, n: int):
        self.buffer = None
        self.is_warm_up = False
        self.n = n

    def get_value(self):
        min = self.buffer.min()
        max = self.buffer.max()
        current = self.buffer[self.n - 1]
        if max != min:
            return (current - min) / (max - min)
        # If no movement return 0.5 which indicates that we have been on average
        return 0.5
