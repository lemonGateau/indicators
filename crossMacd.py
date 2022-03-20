import pandas as pd

from .common.indicator_funcs import *
from .cross import Cross
from .strategy import Strategy

class CrossMacd(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("macd")

    def generate_macds(self, close, ema_terms=[12, 25], signal_term=9):
        ema1 = generate_ema(close, ema_terms[0])
        ema2 = generate_ema(close, ema_terms[1])

        macd = ema1 - ema2
        signal = generate_sma(macd, signal_term)
 
        self.cross = Cross(macd, signal)

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

