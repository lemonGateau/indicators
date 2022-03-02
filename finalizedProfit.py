import pandas as pd

from common.indicator_funcs import *
from common.plot_funcs import plot_df
from common.print_funcs import *
from .strategy import Strategy

class FinalizedProfit(Strategy):
    def __init__(self, df_close, profit_ratio=0.2, loss_ratio=0.05):
        self.df_close = df_close

        self.set_profit_ratio(profit_ratio)
        self.set_loss_ratio(loss_ratio)

        self.set_latest_buy_price(None)
        self.set_strategy_name("fp")

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        # 利確
        if should_realize_profit(self.df_close[i], self.latest_buy_price, self.profit_ratio):
            return True

        # 損切り
        if should_stop_loss(self.df_close[i], self.latest_buy_price, self.loss_ratio):
            return True

        return False

    def should_buy(self, i):
        return False

    def set_profit_ratio(self, profit_ratio):
        self.profit_ratio = profit_ratio

    def set_loss_ratio(self, loss_ratio):
        self.loss_ratio = loss_ratio

    def build_df_indicator(self):
        return pd.DataFrame(data={
            "Close": self.df_close
        }, index=self.df_close.index)
