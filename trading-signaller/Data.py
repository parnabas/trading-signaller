import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import time
from dotenv import load_dotenv
from pathlib import Path

file_name = "C:/Users/wen_z/Documents/GitHub/trading-signaller/trading-signaller/text.xlsx"
start_time = time.time()
seconds = 1
class EnvironmentVars:
    dotenv_path : Path = Path("src/constants.env")
    TELEGRAM_BOT_URL : str
    SIGNALLING_CHAT_ID : str
    CURRENCYPAIRS_NAMES_DIR : str

    def __init__(self) -> None:
        EnvironmentVars.init_env_variables()

    @classmethod
    def __query_class_attributes(cls) -> bool:
        if (cls.TELEGRAM_BOT_URL == None or cls.SIGNALLING_CHAT_ID == None 
        or cls.CURRENCYPAIRS_NAMES_DIR == None):
            return False
        return True

    @classmethod
    def init_env_variables(cls) -> None:
        print("Loading environment variables...")
        load_dotenv(dotenv_path = EnvironmentVars.dotenv_path)
        cls.TELEGRAM_BOT_URL = os.getenv("TELEGRAM_BOT_URL")
        cls.SIGNALLING_CHAT_ID = os.getenv("SIGNALLING_CHAT_ID")
        cls.CURRENCYPAIRS_NAMES_DIR = os.getenv("CURRENCYPAIRS_NAMES_DIR")
        try:
            if (not EnvironmentVars.__query_class_attributes()):
                raise Exception("@Data.EnvironmentVars.init_env_variables(): Error! Failed to load environment variables")
        except Exception as e:
            raise(e)
        print("Environment variables successfully loaded!")

class Data(object):
    """Main class for financial data related functionalities"""
    def __init__(self) -> None:
        pairs = __get_currency_pairs(self)
        
    def __get_currency_pairs(self) -> Dict[str, list[TA_Handler]]: 
        currency_pair_names : list[str]
        time_frame_names : list[str]

        #Get names of currency pairs
        try:
            with open(EnvironmentVars.CURRENCYPAIRS_NAMES_DIR) as file:    
               currency_pair_names = json.load(file)
        except Exception as e:
            print("Exception thrown @ Data.__get_currency_pairs: File failed to load. Reason:")
            raise(e)

        #Get currency pairs for each time frame

        
    
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