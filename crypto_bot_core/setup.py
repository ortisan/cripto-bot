from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='crypto-bot-core',
    version='0.0.1',
    packages=[''],
    url='https://github.com/ortisan/crypto-bot',
    license='',
    author='Marcelo Ortiz de Santana',
    author_email='tentativafc@gmail.com',
    description='This package contains a trade analytic tools. In development...',
    long_description=long_description,
    install_requires=[
      'Backtesting==0.3.3',
      'numpy>=1.21.4',
      'pandas>=1.3.5',
      'pandas-datareader>=0.10.0',
      'pytz>=2021.3',
      'ta>=0.8.0',
    ],
)