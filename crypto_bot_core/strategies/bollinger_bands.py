
from backtesting import Strategy
from backtesting.lib import crossover
from ta.volatility import BollingerBands

class BollingerBandsCross(Strategy):
    # window size for mean and std
    window = 10
    # number of deviations
    deviations = 2
    
    def init(self):
        self.indicator_bb = BollingerBands(close=self.data.Close, window=self.window, window_dev=self.deviations)
    
    def next(self):
        # Close crosses lower band, we need buy
        if crossover(self.data.Close, self.indicator_bb.indicator_bb.bollinger_lband()):
            self.position.close()
            self.buy()

        # Close crosses upper band, we need sell
        elif crossover(self.data.Close, self.indicator_bb.indicator_bb.bollinger_hband()):
            self.position.close()
            self.sell()