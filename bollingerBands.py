import pandas as pd

from .common.indicator_funcs import *
from .strategy import Strategy

class BollingerBands(Strategy):
    def __init__(self, close, term=25):
        self.df = pd.DataFrame()

        self.close = close
        self.std   = close.rolling(term).std()
        self.sma   = generate_sma(close, term)

        self.generate_upper(coef=3)
        self.generate_lower(coef=3)

        self.set_latest_buy_price(None)
        self.set_strategy_name("bb")

        # print(self.df)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return self.close[i] > self.upper[i]

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.close[i] < self.lower[i]

    def generate_upper(self, coef=3):
        self.upper = self.sma + coef * self.std

    def generate_lower(self, coef=3):
        self.lower = self.sma - coef * self.std

    def get_upper(self):
        return self.upper

    def get_lower(self):
        return self.lower

    def build_df_indicator(self):
        return pd.DataFrame(data={
            "Close" : self.close,
            "middle": self.sma  ,
            "upper" : self.upper,
            "lower" : self.lower
            }, index=self.close.index)
