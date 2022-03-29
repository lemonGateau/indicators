import pandas as pd

from .common.indicator_funcs import *
from .cross import Cross
from .strategy import Strategy

class CrossSma(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("sma")

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.cross.should_buy(i)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return self.cross.should_sell(i)

    def build_indicators(self):
        return self.cross.build_indicators()

    def generate_indicators(self, close, terms=[12, 25]):
        self._generate_smas(close, terms)

    def _generate_smas(self, close, terms=[12, 25]):
        sma1 = generate_sma(close, terms[0])
        sma2 = generate_sma(close, terms[1])

        self.cross = Cross(sma1, sma2)
