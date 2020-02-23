#!/usr/bin/python3

import pandas as pd
import xlrd
from pandas import DataFrame
import sys

inp = sys.stdin.read()
string = inp.split(" ")
email = string[0]
ticker = string[1]


loc = 'test.xlsx'

wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0)

num = sheet.nrows

emails = []
tickers = []
prices = []
quants = []

i = 1

if len(string) < 3:
	print("here")
	while i < num:
		if sheet.cell_value(i, 0) != email:
			emails.append(sheet.cell_value(i, 0))
			tickers.append(sheet.cell_value(i, 1))
			prices.append(sheet.cell_value(i, 2))
			quants.append(sheet.cell_value(i, 3))
		i = i + 1

else:
	print("here2")
	while i < num:
		if sheet.cell_value(i, 0) != email or sheet.cell_value(i, 1) != ticker:
			emails.append(sheet.cell_value(i, 0))
			tickers.append(sheet.cell_value(i, 1))
			prices.append(sheet.cell_value(i, 2))
			quants.append(sheet.cell_value(i, 3))
		i = i + 1


# emails = ['jack.roth@yale.edu', 'david.schwartz@yale.edu', 'benjamin.wang@yale.edu', 'juan.valencia@yale.edu']
# tickers = ['AAPL', 'MSFT', 'BLK', 'GS']
# prices = [160.9, 190.81, 480.84, 203.84]
# quants = [4, 100, 45, 72]







df = DataFrame({'Email': emails, 'Ticker': tickers, 'Buying Price': prices, 'Quantity': quants})

df.to_excel('test2.xlsx', sheet_name = 'sheet1', index=False)