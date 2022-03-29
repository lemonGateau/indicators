from collections import OrderedDict

from .strategy import Strategy

class CombinationStrategy(Strategy):
    def __init__(self, buy_strategies, sell_strategies):
        # 深いコピー
        self.strategies = buy_strategies + sell_strategies
        # 重複要素削除
        self.strategies = list(OrderedDict.fromkeys(self.strategies))

        self.buy_strats  = buy_strategies
        self.sell_strats = sell_strategies

        self.set_latest_buy_price(None)
        self.set_strategy_name()

    def should_buy(self, i):
        for strat in self.buy_strats:
            if strat.should_buy(i):
                # print(strat.get_strategy_name(), end="※ ")
                return True
        return False

    def should_sell(self, i):
        for strat in self.sell_strats:
            if strat.should_sell(i):
                # print(strat.get_strategy_name(), end="※ ")
                return True
        return False

    def build_indicators(self):
        dfs = []
        for strat in self.strategies:
            dfs.append(strat.build_indicators())

        return dfs

    def set_strategy_name(self, strat_names=None):
        if type(strat_names) is str:
            self.strat_name = strat_names
            return

        if strat_names:
            self.strat_name = '_'.join(strat_names)
            return

        buy_strat_names  = []
        for strat in self.buy_strats:
            buy_strat_names.append(strat.get_strategy_name())

        sell_strat_names = []
        for strat in self.sell_strats:
            sell_strat_names.append(strat.get_strategy_name())

        self.strat_name = '_'.join(buy_strat_names) + '--' + '_'.join(sell_strat_names)

    def set_latest_buy_price(self, buy_price):
        for strat in self.strategies:
            strat.set_latest_buy_price(buy_price)
