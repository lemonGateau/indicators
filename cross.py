import pandas as pd

from .common.indicator_funcs import *
from .strategy import Strategy

class Cross():
    def __init__(self, ma1, ma2):
        self.ma1 = ma1
        self.ma2 = ma2

    def should_sell(self, i):
        return is_crossover(self.ma1[i-1:i+1], self.ma2[i-1:i+1])

    def should_buy(self, i):
        return is_crossover(self.ma2[i-1:i+1], self.ma1[i-1:i+1])

    def build_df_indicator(self):
        return pd.DataFrame(data={
            "ma1": self.ma1,
            "ma2": self.ma2
        }, index=self.ma1.index)
