import pandas as pd
import time
from dotenv import load_dotenv
from pathlib import Path
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
        print("Environment variables successfully loaded!")

class Data(object):
    currency_pairs : list[str]
    granularities : list[str]
    
    """Main class for financial data related functionalities"""
    def __init__(self) -> None:
        currency_pairs, granularities = __get_currency_pairs(self)
        client = oandapyV20.API(EnvironmentVars.ACCESS_TOKEN)
        
    def __get_currency_pairs(self) -> tuple[list[str], list[str]]: 
        #Get desired currency pairs and time frames
        try:
            with open(EnvironmentVars.PARAMS_DIR) as file:    
               return json.load(file)["currency_pairs"], json.load(file)["granularities"]
        except Exception as e:
            print("Exception thrown @ Data.__get_currency_pairs: File failed to load. Reason:")
            raise(e)

    #Output example: https://oanda-api-v20.readthedocs.io/en/latest/endpoints/instruments/instrumentlist.html
    def get_past_5_OHLC(self, currency_pair, granularity):
        param = {5, granularity}
        r = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
        client.request(r)
        return r.response["candles"]




    