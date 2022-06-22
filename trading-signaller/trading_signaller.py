import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import requests
from Data import EnvironmentVars, Data, CandleCache


API : str = "api-fxtrade.oanda.com"
STREAM_API : str = "stream-fxtrade.oanda.com"
ACCESS_TOKEN : str = "2d1604a423e54b47bf0678b1cec8e6c6-47058592ffbd025c7e07c3e5be20dcfd"
ACCOUNT_ID : str = "101-003-22586265-001"
client = oandapyV20.API(ACCESS_TOKEN)

granularities = ["M15", "H1", "H2", "H4", "H6", "H12", "D", "W"]

params = {
  "count": 5,
  "granularity": "H4"
}


def main():
    EnvironmentVars()
    Data.update_excel_sheet()


if __name__ == "__main__":
    main()
