import pandas as pd

from .common.indicator_funcs import *
from .strategy import Strategy

class Momentum(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("mom")

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        # ゼロラインを超えた時
        if is_crossover(self.moment[i-1:i+1], self.baseline[i-1:i+1]):
            return True

        if self.moment[i] <= self.baseline[i] and is_crossover(self.moment[i-1:i+1], self.signal[i-1:i+1]):
            return True

        return False

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if is_crossover(self.baseline[i-1:i+1], self.moment[i-1:i+1]):
            return True

        if self.moment[i] >= self.baseline[i] and is_crossover(self.signal[i-1:i+1], self.moment[i-1:i+1]):
            return True

        return False

    def build_indicators(self):
        return pd.DataFrame(data={
            "moment"    : self.moment,
            "mom_signal": self.signal,
            "mom_base"  : self.baseline
            }, index=self.moment.index)

    def generate_indicators(self, close, terms=[26, 10], base_value=0):
        self._generate_moment(close, terms[0])
        self._generate_signal(terms[1])
        self._generate_baseline(base_value)

    def _generate_moment(self, close, mom_term=26):
        self.moment = close - close.shift(mom_term)

    def _generate_signal(self, signal_term=10):
        self.signal = generate_sma(self.moment, signal_term)

    def _generate_baseline(self, base_value=0):
        # self.baseline =  pd.DataFrame(data=[base_value]*len(self.moment), index=self.moment.index, columns=["base"])["base"]
        self.baseline =  pd.Series(data=[base_value]*len(self.moment), index=self.moment.index, name="base")

