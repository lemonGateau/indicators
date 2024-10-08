from pandas_datareader import data
import pandas as pd
import datetime

from .common.indicator_funcs import *
from .strategy import Strategy

class Dmi(Strategy):
    def __init__(self):
        self.set_latest_buy_price(None)
        self.set_strategy_name("dmi")

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        if self.adx[i] > 25 and is_crossover(self.p_di[i-1:i+1], self.m_di[i-1:i+1]):
            return True

        return False

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if self.adx[i] > 25 and is_crossover(self.m_di[i-1:i+1], self.p_di[i-1:i+1]):
            return True

        return False

    def build_indicators(self):
        return pd.DataFrame(data={
            "plus_di" : self.p_di,
            "minus_di": self.m_di,
            "adx"     : self.adx
            }, index=self.p_di.index)

    def generate_indicators(self, close, high, low, terms=[14, 25]):
        self._compute_tr(close, high, low)
        self._compute_dms(high, low)
        self._compute_dis(terms[0])
        self._compute_dx()
        self._compute_adx(terms[0])
        self._compute_adxr(terms[1])

    def _compute_tr(self, close, high, low):
        t1 = high          - low
        t2 = high          - close.shift()
        t3 = close.shift() - low

        self.tr = pd.concat([t1, t2, t3], axis=1).max(axis=1)

    def _compute_dms(self, high, low):
        dms = pd.DataFrame()

        dms["p_dm"] = high        - high.shift()
        dms["m_dm"] = low.shift() - low

        self.p_dm, self.m_dm = self._adjust_dms(dms)

    def _adjust_dms(self, df):
        # 一致なら両方0
        df.loc[df["p_dm"] == df["m_dm"], ["p_dm", "m_dm"]] = 0

        # 0未満なら0
        df.loc[df["p_dm"] < 0, "p_dm"] = 0
        df.loc[df["m_dm"] < 0, "m_dm"] = 0

        # 小さい方は0
        df.loc[df["p_dm"] < df["m_dm"] , "p_dm"] = 0
        df.loc[df["m_dm"] < df["p_dm"] , "m_dm"] = 0

        return df["p_dm"], df["m_dm"]

    def _compute_dis(self, adx_term=14):
        sum_pdm = self.p_dm.rolling(adx_term).sum()
        sum_mdm = self.m_dm.rolling(adx_term).sum()
        sum_tr  = self.tr.rolling(adx_term).sum()

        self.p_di = sum_pdm / sum_tr * 100
        self.m_di = sum_mdm / sum_tr * 100

    def _compute_dx(self):
        self.dx = abs(self.p_di - self.m_di) / (self.p_di + self.m_di) * 100

    def _compute_adx(self, adx_term=14):
        self.adx  = generate_ema(self.dx, adx_term)

    def _compute_adxr(self, adxr_term=25):
        self.adxr = generate_sma(self.adx, adxr_term)

