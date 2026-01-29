import logging
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)  # insert(0) so it wins over other paths

import MetaTrader5 as mt5
from strategytester5.tester import StrategyTester, TIMEFRAME2STRING_MAP
import json
import os
from datetime import datetime

if not mt5.initialize(): # Initialize MetaTrader5 instance
    print(f"Failed to Initialize MetaTrader5. Error = {mt5.last_error()}")
    mt5.shutdown()
    quit()

# Get path to the folder where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(BASE_DIR, "tester_config_single_instrument.json"), 'r', encoding='utf-8') as file: # reading a JSON file
        # Deserialize the file data into a Python object
        configs_json = json.load(file)
except Exception as e:
    raise RuntimeError(e)

tester_configs = configs_json["tester"]
tester = StrategyTester(tester_config=tester_configs, mt5_instance=mt5, logging_level=logging.INFO) # very important

# -------------  global variables ----------------

symbols = tester_configs["symbols"]
timeframes = [mt5.TIMEFRAME_M15, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_D1]

# ---------------------------------------------------------

def on_tick():

    for symbol in symbols:
        for tf in timeframes:

            rates = tester.copy_rates_from_pos(symbol=symbol, timeframe=tf, start_pos=0, count=5)

            if rates is None:
                continue

            if len(rates) ==0:
                continue

            # open_price = rates[-1]["open"] # current opening price, the latest one in the array
            # time = datetime.fromtimestamp(rates[-1]["time"])

            # print(f"{time} : symbol: {symbol} tf: {TIMEFRAME2STRING_MAP[tf]} | Current candle's opening = {open_price:.5f}");


tester.OnTick(ontick_func=on_tick) # very important!

