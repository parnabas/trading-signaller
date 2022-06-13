import win32com.client
import os

# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}




# Create an instance of the Excel Application & make it visible.
ExcelApp = win32com.client.GetActiveObject("Excel.Application")
ExcelApp.Visible = True

# Open the desired workbook
excel_wkbk = ExcelApp.Workbooks(1)
print(excel_wkbk.Name)


# set the value property equal to the record array.
ExcelApp.Range("F2:I5").Interior.ColorIndex = 3;

