# Crypto Bot

## Env Config

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