import win32com.client
import os
import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta
import time

# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}

file_name = "C:/Users/wen_z/Documents/GitHub/trading-signaller/trading-signaller/text.xlsx"
start_time = time.time()
seconds = 1



# Create an instance of the Excel Application & make it visible.
ExcelApp = win32com.client.GetActiveObject("Excel.Application")
ExcelApp.Visible = True

print(os.listdir('.'))
# Open the desired workbook
workbook = ExcelApp.Workbooks.Open("whyisntthisworking.xlsx")

# Take the data frame object and convert it to a recordset array
rec_array = data_frame.to_records()

# Convert the Recordset Array to a list. This is because Excel doesn't recognize 
# Numpy datatypes.
rec_array = rec_array.tolist()

# It will look something like this now.
# [(1, 'Apple', Decimal('2'), 4.0), (2, 'Orange', Decimal('3'), 5.0), (3, 'Peach', 
# Decimal('5'), 5.0), (4, 'Pear', Decimal('6'), 5.0)]

# set the value property equal to the record array.
ExcelApp.Range("F2:I5").Value = rec_array


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