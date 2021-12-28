
## Commands

```sh
# Faz download dos dados
freqtrade download-data --exchange binance -t 15m
# Inicia o trade usando a estrategia BBRSINaiveStrategy
freqtrade trade --logfile ./user_data/logs/freqtrade.log --config ./user_data/config.json --strategy BBRSINaiveStrategy
# Faz o backtesting
freqtrade backtesting --config ./user_data/config.json --datadir ./user_data/data/binance --export trades --stake-amount 100 -s BBRSINaiveStrategy -i 15m
# Plota os resultados da estratégia (pontos de compra/venda)
freqtrade plot-dataframe --strategy BBRSINaiveStrategy -p DOGE/USDT -i 15m
```