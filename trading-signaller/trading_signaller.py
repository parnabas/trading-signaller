import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import requests
import time
from Data import EnvironmentVars, Data, CandleCache



def main():
    EnvironmentVars()
    cycle_count = 0
    while True:
        start = time.time()
        Data.update_excel_sheet()
        end = time.time()
        time.sleep(2.0)
        cycle_count += 1
        print("Cycle (%d), call took %.2f seconds" % (cycle_count, end - start))



if __name__ == "__main__":
    main()
