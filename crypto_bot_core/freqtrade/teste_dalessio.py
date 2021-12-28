import pygad
import talib as ta
from talib import LINEARREG_ANGLE

import pandas as pd
import freqtrade.vendor.qtpylib.indicators as qtpylib
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
    8. Angle Linear regression(15=0, 30=1, 45=2, 60=3)
    9. Period gene 8 (5=0, 10=1, 20=2)
    10. Relational Operator of gene 8 (<=  =0, > =1)
    """
    def __init__(self, genes: list):
        self.genes = genes

    def get_decision(self, genes: list):
        gen1 = genes[0]
        period = None
        if (gen1 == 0):
            period = 5
        elif (gen1 == 1):
            period = 10
        else:
            period = 20

        gen2 = genes[1]
        trend_function = None
        if (gen2 == 0):
            trend_function = lambda df: ta.SMA(df, timeperiod=period)
        else:
            trend_function = lambda df: ta.EMA(df, timeperiod=period)

        gen4 = genes[3]
        price_function = None
        if (gen4 == 0):
            price_function = lambda df: df["close"]
        else:
            price_function = lambda df: (df["high"] + df["low"] + df["close"]) / 3

        gen3 = genes[2]
        decision1 = None
        if (gen3 == 0):
            decision1 = lambda df: trend_function(df) < price_function(df)
        elif (gen3 == 1):
            decision1 = lambda df: trend_function(df) <= price_function(df)
        else:
            decision1 = lambda df: trend_function(df) > price_function(df)
            
        gen5 = genes[4]
        stds = None
        if (gen5 == 0):
            stds = 1
        elif (gen5 == 1):
            stds = 2
        else:
            stds = 3    

        lower_band = lambda df: qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=stds)["lower"]
        upper_band = lambda df: qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=stds)["upper"]

        gen7 = genes[6]
        price_function2 = None
        if (gen7 == 0):
            price_function2 = lambda df: df["close"]
        else:
            price_function2 = lambda df: (df["high"] + df["low"] + df["close"]) / 3
            
        gen6 = genes[5]
        decision2 = None
        if (gen6 == 0):
            decision2 = lambda df: qtpylib.crossed_above(price_function2(df), lower_band(df))
        else:
            decision2 = lambda df: qtpylib.crossed_below(price_function2(df), upper_band(df))
            
        gen8 = genes[7]
        angle = None
        if (gen8 == 0):
            angle = 15
        if (gen8 == 1):
            angle = 30
        if (gen8 == 2):
            angle = 45
        else:
            angle = 60    

        gen9 = genes[8]
        period_linear_regression = None
        if (gen9 == 0):
            period_linear_regression = 5
        elif (gen9 ==1):
            period_linear_regression = 10
        else:
            period_linear_regression = 20        

        angle_linear_regression = lambda df: LINEARREG_ANGLE(df["close"], timeperiod=period_linear_regression)

        gen10 = genes[9]
        decision3 = None
        if (gen10 == 0):
            decision3 = lambda df: angle_linear_regression(df) <= angle
        if (gen10 == 0):
            decision3 = lambda df: angle_linear_regression(df) > angle

        return lambda df: (decision1(df)) & (decision2(df)) & (decision3(df))
        

    def get_decisions(self):
        genes_buy = self.genes[0:10]
        decision_buy = self.get_decision(genes_buy)

        genes_sell = self.genes[10:]
        decision_sell = self.get_decision(genes_sell)

        return (decision_buy, decision_sell)

import pygad
import numpy as np

class AlgoCripoBot(object):
    def __init__(self, backtesting, strategy) -> None:
        self.backtesting = backtesting
        self.strategy = strategy
    
    def start_learning(self):
        gene_space = [
            # buy
            {'low': 0, 'high': 1}, 
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 1},
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 1},
            {'low': 0, 'high': 1},
            {'low': 0, 'high': 3},
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 1},
            # sell
            {'low': 0, 'high': 1}, 
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 1},
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 1},
            {'low': 0, 'high': 1},
            {'low': 0, 'high': 3},
            {'low': 0, 'high': 2},
            {'low': 0, 'high': 1}
        ]

        def fitness_func(solution, solution_idx):
            strategy_factory = StrategyFactory(solution)
            decision_buy, decision_sell = strategy_factory.get_decisions()
            self.strategy.set_decisions(decision_buy, decision_sell)
            self.backtesting.start()
            results = self.backtesting.results
            print(f'Idx {solution_idx}, Solution {solution}, profit {results.get("strategy_comparison")[0].get("profit_sum_pct")}')
            return results.get("strategy_comparison")[0].get("profit_sum_pct")

        def on_start(ga_instance):
            print("on_start()")

        def on_fitness(ga_instance, population_fitness):
            print("on_fitness()")

        def on_parents(ga_instance, selected_parents):
            print("on_parents()")

        def on_crossover(ga_instance, offspring_crossover):
            print("on_crossover()")

        def on_mutation(ga_instance, offspring_mutation):
            print("on_mutation()")

        def on_generation(ga_instance):
            print("on_generation()")

        def on_stop(ga_instance, last_population_fitness):
            print("on_stop()")

        ga_instance = pygad.GA(
            num_generations=1000,
            num_parents_mating=50,
            fitness_func=fitness_func,
            sol_per_pop=50,
            num_genes=len(gene_space),
            gene_space = gene_space,
            gene_type=int,
            on_start=on_start,
            on_fitness=on_fitness,
            on_parents=on_parents,
            on_crossover=on_crossover,
            on_mutation=on_mutation,
            on_generation=on_generation,
            on_stop=on_stop,
            allow_duplicate_genes=False,
            stop_criteria=["reach_10", "saturate_15"]
        )

        ga_instance.run()
        ga_instance.plot_fitness()


if __name__ ==  "__main__":
  args = [
        'backtesting',
        '--config', 'config.json',
        '--strategy', 'GeneticAlgo',
        '--export', 'none'
    ]

  # Import here to avoid loading backtesting module when it's not used
  from freqtrade.commands import Arguments
  from freqtrade.commands.optimize_commands import setup_optimize_configuration, start_backtesting
  from freqtrade.enums import RunMode
  from freqtrade.optimize.backtesting import Backtesting

  # Initialize configuration
  pargs = Arguments(args).get_parsed_arg()
  config = setup_optimize_configuration(pargs, RunMode.BACKTEST)
  # Initialize backtesting object
  backtesting = Backtesting(config)
  strategy = backtesting.strategylist[0]

  algoCriptoBot = AlgoCripoBot(backtesting, strategy)
  algoCriptoBot.start_learning()

#   backtesting.start()
#   backtesting.results