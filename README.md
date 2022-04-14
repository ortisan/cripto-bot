# Crypto Bot

Strategies and notebooks for [freqtrade](https://www.freqtrade.io)

## Env Config

Install [Freqtrade](https://www.freqtrade.io/en/stable/installation/)

Configure **userdir**

```sh
# Step 1 - Initialize user folder
freqtrade create-userdir --userdir user_data

# Step 2 - Create a new configuration file
freqtrade new-config --config config.json
```

Install new Env:

```sh
conda create -n crypto-bot python=3.9.0
conda activate crypto-bot
pip install -r requirements.txt
```

Install core lib:

```sh
cd crypto_bot_core
pip install -e . --user
cd -
```

## Running Env

```sh
conda activate crypto-bot
jupyter notebook notebooks
```

## Other commands

Deactivate env:

```sh
conda deactivate
```

Delete env:

```sh
conda env remove -n crypto-bot
```