import pandas as pd
import talib.abstract as ta

class StrategyFactory(object):
  """
  1. Period gene 2 (5=0, 10=1, 20=2)
  1. Trend type (SMA=0, EMA=1)  
  3. Relational Operator (< =0, <=  =1, > =2)
  4. Price used in relation (close=0, (H+L+C)/3=1)
  5. STD Bollinger Band (1=0, 2=1, 3=2)
  6. Cross Above (Yes=0, No=1)
  7. Price used in relation (close=0, (H+L+C)/3=1)
  8. Angle Linear Correlation(15=0, 30=1, 45=2, 60=3)
  9. Relational Operator of gene 8 (< =0, <=  =1, > =2)
  10. Market Action (0 buy, 1 sell)
  """
  def __init__(self, genes: list):
    self.genes = genes
  
  def get_strategy(self):

    gen1 = self.genes[0]
    period = None
    if (gen1 == 0):
      period = 5
    elif (gen1 == 1):
      period = 10
    else:
      period = 20
    
    gen2 = self.genes[1]
    trend_function = None
    if (gen2 == 0):
      trend_function = lambda df: ta.SMA(df, timeperiod=period)

    gen3 = self.genes[2]







