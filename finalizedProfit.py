import pandas as pd

from .common.indicator_funcs import *
from .strategy import Strategy

class FinalizedProfit(Strategy):
    def __init__(self, close):
        self.close = close

        self.set_latest_buy_price(None)
        self.set_strategy_name("fp")

    def should_buy(self, i):
        return False

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        # 利確
        if should_realize_profit(self.close[i], self.latest_buy_price, self.profit_ratio):
            return True

        # 損切り
        if should_stop_loss(self.close[i], self.latest_buy_price, self.loss_ratio):
            return True

        return False

    def build_indicators(self):
        return pd.DataFrame(data={
            "Close": self.close
        }, index=self.close.index)

    def generate_indicators(self, profit_ratio=0.2, loss_ratio=0.05):
        self._set_profit_ratio(profit_ratio)
        self._set_loss_ratio(loss_ratio)

    def _set_profit_ratio(self, profit_ratio=0.2):
        self.profit_ratio = profit_ratio

    def _set_loss_ratio(self, loss_ratio=0.05):
        self.loss_ratio   = loss_ratio
