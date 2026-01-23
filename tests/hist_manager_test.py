from strategytester5.hist.manager import HistoryManager
from strategytester5.validators.tester_configs import TesterConfigValidators

history_dir = "Test History"
    
if __name__ == "__main__":

    tester_config: dict = {
        "bot_name": "test EA",
        "deposit": 1000,
        "leverage": "1:100",
        "timeframe": "H1",
        "start_date": "01.01.2025 00:00",
        "end_date": "31.12.2025 00:00",
        "modelling": "1-minute-ohlc",
        # "modelling": "new_bar",
        "symbols": ["EURUSD", "GBPUSD", "USDCAD"]
    }

    tester_config = TesterConfigValidators.parse_tester_configs(tester_config)
        
    start_dt = tester_config["start_date"]
    end_dt   = tester_config["end_date"]
    symbols = tester_config["symbols"]
    timeframe = tester_config["timeframe"]
    modelling = tester_config["modelling"]


    import MetaTrader5 as mt5
    

    if not mt5.initialize():
        print("Failed to initialize MetaTrader5, Error = ", mt5.last_error())
        quit()

    hist_manager = HistoryManager(mt5_instance=mt5,
                                start_dt=start_dt,
                                end_dt=end_dt,
                                symbols=symbols,
                                timeframe=timeframe)

    hist_manager.fetch_history(modelling=modelling)
    hist_manager.synchronize_timeframes()