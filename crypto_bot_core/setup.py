from setuptools import setup

with open("README.md", "r") as rf:
    long_description = rf.read()

with open("requirements.txt", "r") as req:
    install_requires = req.read().splitlines()

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
    install_requires=install_requires
)