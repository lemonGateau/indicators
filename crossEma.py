import pandas as pd

from .common.indicator_funcs import *
from .cross import Cross
from .strategy import Strategy

class CrossEma(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("ema")

    def generate_emas(self, close, terms=[12, 25]):
        ema1 = generate_ema(close, terms[0])
        ema2 = generate_ema(close, terms[1])

        self.cross = Cross(ema1, ema2)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return self.cross.should_sell(i)

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.cross.should_buy(i)

    def build_df_indicator(self):
        return self.cross.build_df_indicator()

