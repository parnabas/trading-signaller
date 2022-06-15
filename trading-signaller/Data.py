import pandas as pd
import os
import json
import time
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass, field
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import requests

class EnvironmentVars:
    dotenv_path : Path = Path("src/constants.env")
    TELEGRAM_BOT_URL : str
    SIGNALLING_CHAT_ID : str
    PARAMS_DIR : str
    API : str
    STREAM_API : str 
    ACCESS_TOKEN : str 
    ACCOUNT_ID : str
    SHEET_DIR : str
    
    currency_pairs : list[str]
    granularities : list[str]

    def __init__(self) -> None:
        EnvironmentVars.init_env_variables()

    @classmethod
    def __query_class_attributes(cls) -> bool:
        if (cls.TELEGRAM_BOT_URL == None or cls.SIGNALLING_CHAT_ID == None 
        or cls.PARAMS_DIR == None or cls.API == None 
        or cls.STREAM_API == None or cls.ACCESS_TOKEN == None
        or cls.ACCOUNT_ID == None or cls.SHEET_DIR == None):
            return False
        return True
    
    @classmethod
    def init_env_variables(cls) -> None:
        print("Loading environment variables...")
        load_dotenv(dotenv_path = EnvironmentVars.dotenv_path)
        cls.TELEGRAM_BOT_URL = os.getenv("TELEGRAM_BOT_URL")
        cls.SIGNALLING_CHAT_ID = os.getenv("SIGNALLING_CHAT_ID")
        cls.PARAMS_DIR = os.getenv("PARAMS_DIR")
        cls.API = os.getenv("API")
        cls.STREAM_API = os.getenv("STREAM_API")
        cls.ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        cls.ACCOUNT_ID = os.getenv("ACCOUNT_ID")
        cls.SHEET_DIR = os.getenv("SHEET_DIR")
        try:
            if (not EnvironmentVars.__query_class_attributes()):
                raise Exception("@Data.EnvironmentVars.init_env_variables(): Error! Failed to load environment variables")
        except Exception as e:
            raise(e)

        try:
            with open(EnvironmentVars.PARAMS_DIR) as file:    
               params = json.load(file)["params"]
        except Exception as e:
            print("Exception thrown @ Data.__get_currency_pairs: File failed to load. Reason:")
            raise(e)
        
        cls.currency_pairs =  params["currency_pairs"]
        cls.granularities = params["granularities"]
        cls.OANDA_CLIENT = oandapyV20.API(cls.ACCESS_TOKEN)

        print("Environment variables successfully loaded!")
        


class CandleData:
    def __init__(self, high : str, low : str, close : str) -> None:
        self.color : str
        self.high : str = high
        self.low : str = low
        self.close : str = close;
    
    def __str__(self) -> str:
        return self.high + " / " + self.low + " / " + self.close

@dataclass(frozen = True)
class CurrencyPairData:
    name : str
    granularity : str
    past_5_candles : list[CandleData] = field(default_factory = list)

    

class Data(object):
    
    """Main class for financial data related functionalities"""
    def __init__(self) -> None:
        pass

    @classmethod
    def get_financial_data(cls) -> dict[str, dict[str, CurrencyPairData]]:
        all_financial_data : dict[str, dict[str, CurrencyPairData]]     #To store all the pairs, granularities and candle data
        for pair in EnvironmentVars.currency_pairs:
            for granularity in EnvironmentVars.granularities:
                pair_granularities_data : dict[str, CurrencyPairData]
                raw_data = Data._get_past_6_OHLC(pair, granularity)
                data = CurrencyPairData()



    #Output example: https://oanda-api-v20.readthedocs.io/en/latest/endpoints/instruments/instrumentlist.html
    @staticmethod
    def _get_past_6_OHLC(currency_pair, granularity) -> list[CandleData]:
        candles_data : list[CandleData]
        params = {"count" : 5, "granularity" : granularity}
        r = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
        EnvironmentVars.OANDA_CLIENT.request(r)
        raw_candles_data : list[dict] = r.response["candles"]

        for item in raw_candles_data:
            candledata = item["mid"]
            candles_data.append(CandleData(candledata["h"], candledata["l"], candledata["c"]))

        #Assign colors to each candle.
        #if the current price is above the previous candle high, reflect a Green
        #if the current price is below the previous candle low, reflect a Red
        #if the current price is between the previous candle high and low, reflect Neutral
        iterator_candles = iter(candles_data)
        


        #Candle will be inserted into the list with the latest candle as the last index.
        #Reverse list so that latest candle will be 0, then -1, -2 so on.
        candles_data.reverse()
        return r.response["candles"]




    