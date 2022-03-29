import pandas as pd

from .strategy import Strategy


class Rsi(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("rsi")

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        if self.rsi[i] < self.buy_ratio:
            return True

        return False

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if self.rsi[i] > self.sell_ratio:
            return True

        return False

    def build_indicators(self):
        return pd.DataFrame(data={
            "rsi": self.rsi
            }, index=self.rsi.index)

    def generate_indicators(self, close, term=15, buy_ratio=0.3, sell_ratio=0.7):
        self._set_buy_ratio(buy_ratio)
        self._set_sell_ratio(sell_ratio)
        self._compute_rsi(close, term)

    def _set_buy_ratio(self, buy_ratio=0.3):
        self.buy_ratio = buy_ratio

    def _set_sell_ratio(self, sell_ratio=0.7):
        self.sell_ratio = sell_ratio

    def _compute_rsi(self, close, term=15):
        df = pd.DataFrame()

        df["diff"] = close.diff()
        df["up"]   = df["diff"]
        df["down"] = df["diff"]

        # upの0未満とdownの0より大を0に
        df["up"].loc[df["up"] < 0]     = 0
        df["down"].loc[df["down"] > 0] = 0

        df["up_sum"]   = df["up"].rolling(term).sum()
        df["down_sum"] = df["down"].rolling(term).sum().abs()

        self.rsi = df["up_sum"] / (df["up_sum"] + df["down_sum"])
