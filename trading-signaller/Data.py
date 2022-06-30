import pandas as pd
import os
import json
import win32com.client
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
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
   
    def __repr__(self) -> str:
        return self.high + " / " + self.low + " / " + self.close

    def __str__(self) -> str:
        return self.high + " / " + self.low + " / " + self.close

@dataclass(frozen = True)
class CurrencyPairData:
    name : str
    granularity : str
    past_5_candles : list[CandleData] = field(default_factory = list)

    def __repr__(self) -> str:
        output : str = ""
        for candle_data in past_5_candles:
            output += candle_data
        return output
    
class CandleCache:
    """Necessary for speeding up getting the financial data."""
    data : dict[str, dict[str, CurrencyPairData]]
    cache_exists : bool = False

    def __init__(self) -> None:
        pass

class Data(object):
    """Main class for financial data related functionalities"""
    currency_pair_basecell : int = 3
    currency_pair_cell_multiplier : int = 6
    granularity_basecell : int = 4
    granularity_cell_multiplier : int = 2 
    red_color = 255 + (80 * 256) + (80 * 256 * 256)
    green_color = 146 + (208 * 256) + (80 * 256 * 256)
    no_color = 255 + (255 * 256) + (255 * 256 * 256)


    def __init__(self) -> None:
        pass

    @staticmethod
    def _rgbToInt(rgb):
        colorInt = rgb[0] + (rgb[1] * 256) + (rgb[2] * 256 * 256)
        return colorInt

    @classmethod
    def get_financial_data(cls) -> dict[str, dict[str, CurrencyPairData]]:
        all_financial_data : dict[str, dict[str, CurrencyPairData]] = dict()      #To store all the pairs, granularities and candle data
        for pair in EnvironmentVars.currency_pairs:     #for each pair
            granularity_pair_data : dict[str, CurrencyPairData] = dict()  
            for granularity in EnvironmentVars.granularities:       #for each granularity      
                pair_granularities_data : dict[str, CurrencyPairData]
                candle_data = Data._get_past_OHLC(pair, granularity)
                granularity_pair_data[granularity] = candle_data
            all_financial_data[pair] = granularity_pair_data
        CandleCache.data = all_financial_data
        CandleCache.cache_exists = True
        return CandleCache.data

    #Output example: https://oanda-api-v20.readthedocs.io/en/latest/endpoints/instruments/instrumentlist.html
    @staticmethod
    def _get_past_OHLC(currency_pair : str, granularity : str) -> list[CandleData]:
        if (not CandleCache.cache_exists):
            candles_data : list[CandleData] = list()
            params = {"count" : 7, "granularity" : granularity}
            r = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
            EnvironmentVars.OANDA_CLIENT.request(r)
            raw_candles_data : list[dict] = r.response["candles"]

            for i in range(0, len(raw_candles_data)):
                candledata = raw_candles_data[i]["mid"]
                candle = CandleData(candledata["h"], candledata["l"], candledata["c"])
                #if next candle closed higher than the current high, next candle color is green
                if i != 0:
                    if raw_candles_data[i - 1]["mid"]["h"] < raw_candles_data[i]["mid"]["c"]:
                        candle.color = "green"
                    elif raw_candles_data[i - 1]["mid"]["l"] <= raw_candles_data[i]["mid"]["c"]:
                        candle.color = "white"
                    else:
                        candle.color = "red"
                candles_data.append(candle)

            #Assign colors to each candle.
            #if the current price is above the previous candle high, reflect a Green
            #if the current price is below the previous candle low, reflect a Red
            #if the current price is between the previous candle high and low, reflect Neutral
            iterator_candles = iter(candles_data)
        
            #Candle will be inserted into the list with the latest candle as the last index.
            #Reverse list so that latest candle will be 0, then -1, -2 so on.
            candles_data.reverse()

            #Delete the last candle[6] once the color of candle[5] has been assigned
            candles_data.pop()  

            return candles_data
        else:
            #if there is existing data cached, only need to update the first candle of each granularity and pair.
            curr_cached_pair_granularity : list[CandleData] = CandleCache.data[currency_pair][granularity]
            params = {"count" : 1, "granularity" : granularity}
            r = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
            EnvironmentVars.OANDA_CLIENT.request(r)
            raw_candles_data : list[dict] = r.response["candles"]
            candledata = raw_candles_data[0]["mid"]
            candle = CandleData(candledata["h"], candledata["l"], candledata["c"])
            #if next candle closed higher than the current high, next candle color is green
            if curr_cached_pair_granularity[1].high < raw_candles_data[0]["mid"]["c"]:
                candle.color = "green"
            elif curr_cached_pair_granularity[1].low <= raw_candles_data[0]["mid"]["c"]:
                candle.color = "white"
            else:
                candle.color = "red"
            CandleCache.data[currency_pair][granularity][0] = candle
            return CandleCache.data[currency_pair][granularity]
            
    @classmethod
    def update_excel_sheet(cls) -> None:
        data : dict[str, dict[str, CurrencyPairData]] = Data.get_financial_data()
        
        # Create an instance of the Excel Application & make it visible.
        ExcelApp = win32com.client.GetActiveObject("Excel.Application")

        # Open the desired sheet
        sheet = ExcelApp.Workbooks(1).Worksheets(1)
        
        for pairs in data:
            curr_y = cls.currency_pair_basecell + cls.currency_pair_cell_multiplier * (list(data).index(pairs))
            sheet.Cells(curr_y, 1).Value = pairs
            for granularities in data[pairs]:
                curr_x = cls.granularity_basecell + cls.granularity_cell_multiplier * (list(data[pairs]).index(granularities))
                for i in range(0, len(data[pairs][granularities])):
                    pair_granularity_data = data[pairs][granularities]
                    sheet.Cells(curr_y + i, curr_x).Value = str(pair_granularity_data[i])
                    if pair_granularity_data[i].color == "green" : sheet.Cells(curr_y + i, curr_x).Interior.color = cls.green_color
                    elif pair_granularity_data[i].color == "red" : sheet.Cells(curr_y + i, curr_x).Interior.color = cls.red_color
                    else: sheet.Cells(curr_y + i, curr_x).Interior.Color = cls.no_color
        sheet.Cells(1,1).Value = "Last Updated : \n" + datetime.now().strftime("%H%MHRS, %SSEC")
                # set the value property equal to the record array.
                #ExcelApp.Range("F2:I5").Interior.ColorIndex = 3;







    