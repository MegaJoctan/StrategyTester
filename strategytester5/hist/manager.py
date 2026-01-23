from strategytester5 import *
from strategytester5.hist import ticks, bars
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from strategytester5.validators._tester_configs import TesterConfigValidators
from datetime import datetime
import time
import os

class HistoryManager:
    def __init__(self,
                mt5_instance: MetaTrader5, 
                symbols: list,
                start_dt: datetime,
                end_dt: datetime,
                max_fetch_workers: int=None,
                max_cpu_workers: int=None,
                history_dir: str = "History"
                ):
        
        self.mt5_instance = mt5_instance
        self.symbols = symbols
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.max_fetch_workers = max_fetch_workers
        self.max_cpu_workers = max_cpu_workers
        self.history_dir = history_dir
    
    """
    def init_worker_mt5():
        global mt5_instance
        import MetaTrader5 as mt5

        if not mt5.initialize():
            raise RuntimeError(f"MT5 init failed in worker: {mt5.last_error()}")
        mt5_instance = mt5
    """
    
    def _fetch_bars_worker(self, symbol: str, timeframe: int) -> dict:

        bars_obtained = bars.fetch_historical_bars(
            which_mt5=self.mt5_instance,
            symbol=symbol,
            timeframe=timeframe,
            start_datetime=self.start_dt,
            end_datetime=self.end_dt
        )
        
        return {
            "symbol": symbol,
            "bars": bars_obtained,
            "size": bars_obtained.height,
            "counter": 0
        }

    def _fetch_ticks_worker(self, symbol: str) -> dict:
        
        ticks_obtained = ticks.fetch_historical_ticks(
            which_mt5=self.mt5_instance, start_datetime=self.start_dt, end_datetime=self.end_dt, symbol=symbol
        )
        
        return {
            "symbol": symbol,
            "ticks": ticks_obtained,
            "size": ticks_obtained.height,
            "counter": 0
        }

    def _gen_ticks_worker(self, symbol: str, out_dir: str) -> dict:
        
        one_minute_bars = bars.fetch_historical_bars(
            which_mt5=self.mt5_instance,
            symbol=symbol,
            timeframe=TIMEFRAMES_MAP["M1"],  # <- use your map key directly
            start_datetime=self.start_dt,
            end_datetime=self.end_dt
        )
        
        ticks_df = ticks.TicksGen.generate_ticks_from_bars(
            bars=one_minute_bars, 
            symbol=symbol,
            symbol_point=0.01, #TODO:
            out_dir=out_dir,
            return_df=True
        )
        
        return {
            "symbol": symbol,
            "ticks": ticks_df,
            "size": ticks_df.height,
            "counter": 0
        }

    def fetch_history(self, modelling: str, timeframe: int):
        
        if max_fetch_workers is None:
            max_fetch_workers = min(32, max(4, len(self.symbols)))
        if max_cpu_workers is None:
            max_cpu_workers = max(1, os.cpu_count() - 1)
            
        ALL_TICKS_INFO = []
        ALL_BARS_INFO = []
        
        if modelling == "real_ticks":
            
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=max_fetch_workers) as executor:
                futs = {executor.submit(self._fetch_ticks_worker, s): s for s in self.symbols}

                for fut in as_completed(futs):
                    sym = futs[fut]
                    try:
                        res = fut.result()              # <- get dict
                        ALL_TICKS_INFO.append(res)
                    except Exception as e:
                        print(f"Failed for {sym}: {e!r}")

            total_ticks = sum(info["size"] for info in ALL_TICKS_INFO)
            print(f"Total real ticks collected: {total_ticks} in {(time.time()-start_time):.2f} seconds.")
        
        elif modelling == "every_tick":
            
            start_time = time.time()
            
            with ProcessPoolExecutor(max_workers=max_cpu_workers) as executor:
                futs = {executor.submit(self._gen_ticks_worker, s, "Simulated Ticks"): s for s in self.symbols}

                for fut in as_completed(futs):
                    sym = futs[fut]
                    try:
                        res = fut.result()              # <- get dict
                        ALL_TICKS_INFO.append(res)
                    except Exception as e:
                        print(f"Failed for {sym}: {e!r}")

            total_ticks = sum(info["size"] for info in ALL_TICKS_INFO)
            print(f"Total ticks generated: {total_ticks} in {(time.time()-start_time):.2f} seconds.")
        
        elif modelling in ("new_bar", "1-minute-ohlc"):
            
            start_time = time.time()
            tf = TIMEFRAMES_MAP["M1"] if modelling == "1-minute-ohlc" else TIMEFRAMES_MAP[timeframe]
            
            with ThreadPoolExecutor(max_workers=max_fetch_workers) as executor:
                futs = {executor.submit(self._fetch_bars_worker, s, tf): s for s in self.symbols}

                for fut in as_completed(futs):
                    sym = futs[fut]
                    try:
                        res = fut.result()              # <- get dict
                        ALL_BARS_INFO.append(res)
                    except Exception as e:
                        print(f"Failed for {sym}: {e!r}")

            total_bars = sum(info["size"] for info in ALL_BARS_INFO)
            print(f"Total bars collected: {total_bars} from '{TIMEFRAMES_MAP_REVERSE[tf]}' timeframe in {(time.time()-start_time):.2f} seconds.")
            
        
