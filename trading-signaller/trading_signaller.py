from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import time



# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

start_time = time.time()
seconds = 1

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > seconds:
        PYEN = TA_Handler(
            symbol="GBPJPY",
            screener="forex",
            exchange="FX_IDC",
            interval=Interval.INTERVAL_15_MINUTES
        )
        analysis = PYEN.get_analysis()
        print("GBPJPY Current Price:" + str(analysis.indicators["close"]))
        start_time = time.time()    