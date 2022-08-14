import numpy as np
import random


class RandomWalk:

    @staticmethod
    def generate(n):
        min_tick = 0.01
        x = np.ones(1, dtype=float)
        for i in range(1, n):
            # Return in % [-1,1]
            r = 0.01*min_tick * random.randrange(-1 / min_tick, 1 / min_tick)
            x_prev = x[i - 1]
            x_new = x_prev * (1.0 + r)
            x = np.append(x, x_new)
        return x
