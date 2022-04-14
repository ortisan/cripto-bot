import pygad
import talib as ta
from talib import LINEARREG_ANGLE

import pandas as pd
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta

from enum import Enum


class DecisionType(Enum):
    Buy = 1
    Sell = 2


class StrategyFactory(object):
    """
    
    Preço fechamento ou Media é maior/menor que a tendência?
    
    1. fast_period gene 2 (5=0, 10=1, 15=2)
    2. Fast MA Type (SMA=0, EMA=1)

    3. fast_period gene 3 (20=0, 30=1, 50=2)
    4. Slow MA Type Trend type (SMA=0, EMA=1)

    5. Cross type (Above=0, Below=1)

    6. ADX Lower Limit (15 = 0, 20 = 1)
    7. ADX Higher Limit (25=0, 30 = 1)

    8. Money Flow Bottom Limit (15=0, 20=1, 25 = 2)   
    9. Money Flow Above Limit (70=0, 80=1, 85 = 2)
    
    10. RSI Below Limit (15=0, 20=1, 25=2, 30=3)
    11. RSI Above Limit (65=0, 70=1, 75=2, 80=3)

    12. Operator Decision 1 And 2 (&=0,|=1)
    13. Operator Decision 2 And 3 (&=0,|=1)
    14. Operator Decision 3 And 4 (&=0,|=1)
    """

    def __init__(self, genes: list):
        self.genes = genes
        
        genes_buy = self.genes[0:14]
        self.indicators_buy, self.decisions_buy = self.__get_indicators_and_decisions(genes_buy, DecisionType.Buy)

        genes_sell = self.genes[14:]
        self.indicators_sell, self.decisions_sell = self.__get_indicators_and_decisions(genes_sell, DecisionType.Sell)

    def __get_indicators_and_decisions(self, genes: list,
                                     decision_type: DecisionType):
        indicators = []

        gen1 = genes[0]
        fast_period = None
        if (gen1 == 0):
            fast_period = 5
        elif (gen1 == 1):
            fast_period = 10
        else:
            fast_period = 15

        gen2 = genes[1]
        fast_type_ma = None
        if (gen2 == 0):
            fast_type_ma = lambda df: {
                f'ma_fast_{decision_type}': ta.SMA(df, period=fast_period)
            }
        else:
            fast_type_ma = lambda df: {
                f'ma_fast_{decision_type}': ta.EMA(df, period=fast_period)
            }
        indicators.append(fast_type_ma)

        gen3 = genes[2]
        slow_period = None
        if (gen3 == 0):
            slow_period = 20
        elif (gen3 == 1):
            slow_period = 30
        else:
            slow_period = 50

        gen4 = genes[3]
        slow_type_ma = None
        if (gen4 == 0):
            slow_type_ma = lambda df: {
                f'ma_slow_{decision_type}': ta.SMA(df, period=slow_period)
            }
        else:
            slow_type_ma = lambda df: {
                f'ma_slow_{decision_type}': ta.EMA(df, period=slow_period)
            }
        indicators.append(slow_type_ma)

        gen5 = genes[4]
        decision_ma_crosses = None
        if (gen5 == 0):
            decision_ma_crosses = lambda df: {
                f'has_ma_crosses_{decision_type}':
                qtpylib.crossed_above(df[f'ma_fast_{decision_type}'], df[
                    f'ma_slow_{decision_type}'])
            }
        else:
            decision_ma_crosses = lambda df: {
                f'has_ma_crosses_{decision_type}':
                qtpylib.crossed_below(df[f'ma_fast_{decision_type}'], df[
                    f'ma_slow_{decision_type}'])
            }
        indicators.append(decision_ma_crosses)

        gen6 = genes[5]
        adx_lower_limit = None
        if (gen6 == 0):
            adx_lower_limit = 15
        else:
            adx_lower_limit = 20

        gen7 = genes[6]
        adx_higher_limit = None
        if (gen7 == 0):
            adx_higher_limit = 20
        else:
            adx_higher_limit = 30

        adx = lambda df: {
            f'adx_{decision_type}':
            ta.ADX(df['high'], df['low'], df['close'], timeperiod=14)
        }
        indicators.append(adx)

        decision_has_trend = lambda df: {
            f'has_trend_{decision_type}':
            (df[f'adx_{decision_type}'] < adx_lower_limit) |
            (df[f'adx_{decision_type}'] > adx_higher_limit)
        }
        indicators.append(decision_has_trend)

        gen8 = genes[7]
        moneyflow_bottom_limit = None
        if (gen8 == 0):
            moneyflow_bottom_limit = 15
        elif (gen8 == 1):
            moneyflow_bottom_limit = 20
        else:
            moneyflow_bottom_limit = 30

        gen9 = genes[8]
        moneyflow_above_limit = None
        if (gen9 == 0):
            moneyflow_above_limit = 70
        elif (gen9 == 1):
            moneyflow_above_limit = 80
        else:
            moneyflow_above_limit = 85

        moneyflow = lambda df: {
            f'money_flow_{decision_type}':
            ta.MFI(df['high'],
                   df['low'],
                   df['close'],
                   df['volume'],
                   timeperiod=14)
        }
        indicators.append(moneyflow)

        decision_volume = lambda df: {
            f'has_volume_pattern_{decision_type}':
            (df[f'money_flow_{decision_type}'] < moneyflow_bottom_limit) |
            (df[f'money_flow_{decision_type}'] > moneyflow_above_limit)
        }
        indicators.append(decision_volume)

        gen10 = genes[9]
        rsi_bottom_limit = None
        if (gen10 == 0):
            rsi_bottom_limit = 15
        elif (gen10 == 1):
            rsi_bottom_limit = 20
        elif (gen10 == 2):
            rsi_bottom_limit = 25
        else:
            rsi_bottom_limit = 30

        gen11 = genes[10]
        rsi_above_limit = None
        if (gen11 == 0):
            rsi_above_limit = 65
        elif (gen11 == 1):
            rsi_above_limit = 70
        elif (gen11 == 2):
            rsi_above_limit = 75
        else:
            rsi_above_limit = 80

        rsi = lambda df: {
            f'rsi_{decision_type}': ta.RSI(df['close'], timeperiod=14)
        }
        indicators.append(rsi)

        decision_momentum = lambda df: {
            f'is_changing_momentum_{decision_type}':
            (df[f'rsi_{decision_type}'] < rsi_bottom_limit) |
            (df[f'rsi_{decision_type}'] > rsi_above_limit)
        }
        indicators.append(decision_momentum)

        gen12 = genes[11]
        decision_crossover_and_trend = None
        # If has ma crossings and/or trends strenght
        if (gen12 == 0):
            decision_crossover_and_trend = lambda df: (df[
                f'has_ma_crosses_{decision_type}'].rolling(5).sum() >= 1) & (
                    df[f'has_trend_{decision_type}'].rolling(5).sum() > 1)
        else:
            decision_crossover_and_trend = lambda df: df[
                f'has_ma_crosses_{decision_type}'].rolling(5).sum() >= 1 | (df[
                    f'has_trend_{decision_type}'].rolling(5).sum() > 1)

        gen13 = genes[12]
        decision_crossover_and_trend_and_volume = None
        if (gen13 == 0):
            decision_crossover_and_trend_and_volume = lambda df: decision_crossover_and_trend(
                df) & (df[f'has_volume_pattern_{decision_type}'].rolling(5).
                       sum() >= 1)
        else:
            decision_crossover_and_trend_and_volume = lambda df: decision_crossover_and_trend(
                df) | (df[f'has_volume_pattern_{decision_type}'].rolling(5).
                       sum() >= 1)

        gen14 = genes[13]
        decision_crossover_and_trend_and_volume_and_momentum = None
        if (gen14 == 0):
            decision_crossover_and_trend_and_volume_and_momentum = lambda df: decision_crossover_and_trend_and_volume(
                df) & (df[f'is_changing_momentum_{decision_type}'].rolling(5).
                       sum() >= 1)
        else:
            decision_crossover_and_trend_and_volume_and_momentum = lambda df: decision_crossover_and_trend_and_volume(
                df) | (df[f'is_changing_momentum_{decision_type}'].rolling(5).
                       sum() >= 1)

        return (indicators, decision_crossover_and_trend_and_volume_and_momentum)

    def populate_indicators(self, df: pd.DataFrame):
        for indicator_lambda in self.indicators_buy:
            dict_indicator = indicator_lambda(df)
            for indicator_name, indicator_value in dict_indicator.items():
                df[indicator_name] = indicator_value
        
        for indicator_lambda in self.indicators_sell:
            dict_indicator = indicator_lambda(df)
            for indicator_name, indicator_value in dict_indicator.items():
                df[indicator_name] = indicator_value
    

        





        


import pygad
import numpy as np


class AlgoCripoBot(object):

    def __init__(self, backtesting, strategy) -> None:
        self.backtesting = backtesting
        self.strategy = strategy

    def start_learning(self):
        gene_space = [
            # buy
            {
                'low': 0,
                'high': 3
            },  #1
            {
                'low': 0,
                'high': 2
            },  #2
            {
                'low': 0,
                'high': 3
            },  #3
            {
                'low': 0,
                'high': 2
            },  #4
            {
                'low': 0,
                'high': 2
            },  #5
            {
                'low': 0,
                'high': 2
            },  #6
            {
                'low': 0,
                'high': 2
            },  #7
            {
                'low': 0,
                'high': 3
            },  #8
            {
                'low': 0,
                'high': 3
            },  #9
            {
                'low': 0,
                'high': 4
            },  #10
            {
                'low': 0,
                'high': 4
            },  #11
            {
                'low': 0,
                'high': 2
            },  #12
            {
                'low': 0,
                'high': 2
            },  #13
            {
                'low': 0,
                'high': 2
            },  #14

            # sell
            {
                'low': 0,
                'high': 3
            },  #1
            {
                'low': 0,
                'high': 2
            },  #2
            {
                'low': 0,
                'high': 3
            },  #3
            {
                'low': 0,
                'high': 2
            },  #4
            {
                'low': 0,
                'high': 2
            },  #5
            {
                'low': 0,
                'high': 2
            },  #6
            {
                'low': 0,
                'high': 2
            },  #7
            {
                'low': 0,
                'high': 3
            },  #8
            {
                'low': 0,
                'high': 3
            },  #9
            {
                'low': 0,
                'high': 4
            },  #10
            {
                'low': 0,
                'high': 4
            },  #11
            {
                'low': 0,
                'high': 2
            },  #12
            {
                'low': 0,
                'high': 2
            },  #13
            {
                'low': 0,
                'high': 2
            },  #14
        ]

        def fitness_func(chromo, idx_chromo):
            strategy_factory = StrategyFactory(chromo)
            self.strategy.set_strategy_factory(strategy_factory)

            self.backtesting.start()
            results = self.backtesting.results
            print(
                f'Idx {idx_chromo}, Solution {chromo}, profit {results.get("strategy_comparison")[0].get("profit_total_pct")}'
            )
            return results.get("strategy_comparison")[0].get(
                "profit_total_pct")

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
            print("Changing generation...")
            if ga_instance.best_solution_generation != -1:
                print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

        def on_stop(ga_instance, last_population_fitness):
            print("on_stop()")

        ga_instance = pygad.GA(
            num_generations=1000,
            num_parents_mating=10,
            fitness_func=fitness_func,
            sol_per_pop=20,
            num_genes=len(gene_space),
            gene_space=gene_space,
            gene_type=int,

            # on_start=on_start,
            # on_fitness=on_fitness,
            # on_parents=on_parents,
            # on_crossover=on_crossover,
            # on_mutation=on_mutation,
            on_generation=on_generation,
            # on_stop=on_stop,
            crossover_probability = 0.1,
            mutation_type="adaptive",
            mutation_probability=[0.25, 0.1],
            save_solutions=True,
            save_best_solutions=True,
            allow_duplicate_genes=False,
            stop_criteria=["reach_5", "saturate_10"])

        ga_instance.run()  # Treinando
        #ga_instance.plot_fitness()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print("Parameters of the best solution : {solution}".format(solution=solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))
        
        print("Top 5 solutions:", ga_instance.solutions[:5])



if __name__ == "__main__":
    args = [
        'backtesting', '--config', 'config.json', '--strategy', 'GeneticAlgo',
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