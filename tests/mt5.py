import MetaTrader5 as mt5
from strategytester5.mt5 import exporter, importer
import os

if not mt5.initialize():
    raise RuntimeError("MetaTrader5 initialization failed")

exporter.account_info(mt5, os.getcwd())
exporter.all_symbol_info(mt5, os.getcwd())


importer.account_info(os.getcwd())
importer.all_symbol_info(os.getcwd())