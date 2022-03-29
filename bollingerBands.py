import pandas as pd

from .common.indicator_funcs import *
from .strategy import Strategy

class BollingerBands(Strategy):
    def __init__(self, close):
        self.close = close

        self.set_latest_buy_price(None)
        self.set_strategy_name("bb")

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.close[i] < self.lower[i]

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return self.close[i] > self.upper[i]

    def build_indicators(self):
        return pd.DataFrame(data={
            "Close" : self.close,
            "middle": self.middle  ,
            "upper" : self.upper,
            "lower" : self.lower
            }, index=self.close.index)

    def generate_indicators(self, term=25, coef=3):
        self.middle = generate_sma(self.close, term)

        std = self.close.rolling(term).std()

        self._generate_upper(std, coef)
        self._generate_lower(std, coef)

    def _generate_upper(self, std, coef=3):
        self.upper = self.middle + std * coef

    def _generate_lower(self, std, coef=3):
        self.lower = self.middle - std * coef
