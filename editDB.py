#!/usr/bin/python3

import pandas as pd
import xlrd
from pandas import DataFrame
import sys

#Takes in email (string), ticker (string), DBFile (string, xlsx file path), newDBFile (string, xlsx file path)
#and creates a new DB file containing all the tuples not containing that email/ticker combination. If 
#ticker is input as None, then all entries tied to that email are removed.
def removeDB(email, ticker, DBFile, newDBFile):
	#if using stdin
	# inp = sys.stdin.read()
	# string = inp.split(" ")
	# email = string[0]
	# ticker = string[1]


	loc = DBFile #must be an xlsx file

	#open database file
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 
	sheet.cell_value(0, 0)

	num = sheet.nrows

	#initialize lists
	emails = []
	tickers = []
	prices = []
	quants = []

	i = 1

	#if len(string) < 3:
	if ticker is None:
		while i < num:
			if sheet.cell_value(i, 0) != email:
				emails.append(sheet.cell_value(i, 0))
				tickers.append(sheet.cell_value(i, 1))
				prices.append(sheet.cell_value(i, 2))
				quants.append(sheet.cell_value(i, 3))
			i = i + 1

	else:
		while i < num:
			if sheet.cell_value(i, 0) != email or sheet.cell_value(i, 1) != ticker:
				emails.append(sheet.cell_value(i, 0))
				tickers.append(sheet.cell_value(i, 1))
				prices.append(sheet.cell_value(i, 2))
				quants.append(sheet.cell_value(i, 3))
			i = i + 1



	df = DataFrame({'Email': emails, 'Symbol': tickers, 'Price': prices, 'Quantity': quants})
	df = df[['Email', 'Symbol', 'Price', 'Quantity']]

	df.to_excel(newDBFile, sheet_name = 'sheet1', index=False)


#Takes in email (string) DBFile (string, xlsx file path)
#and returns a pandas dataframe containing all the tuples containing that email.
def getFromDB(email, DBFile):
	#if using stdin
	# inp = sys.stdin.read()
	# string = inp.split(" ")
	# email = string[0]

	### OLD DAVID CODE ###
	# loc = DBFile

	# df = pd.read_excel(loc, sheet_name = None)

	# for key in df:
	# 	dfs = (df[key].head())


	# df_list = dfs.loc[dfs['Email'] == email]

	# #print(df_list)

	# return df_list

	### NEW YUXUAN CODE ###
	# DBFile = 'test.xlsx'
	# email = 'david.schwartz@yale.edu'
	names = ['Email', 'Symbol', 'Price', 'Quantity']
	# note: if our excel already has headers, the filter will remove the extra
	# row anyway, so we assume there are no headers and add the header above
	df = pd.read_excel(DBFile, sheet_name = 0, header=None, names=names)


	return df[df['Email'] == email]

#Takes in email (string), ticker (string), new_quantity(int), DBFile (string, xlsx file path), newDBFile (string, xlsx file path)
#and creates a new DB file containing the updated quantity for that email/ticker combination.
def changeQuantity(email, ticker, new_quantity, DBFile, newDBFile):
	#if using stdin
	# inp = sys.stdin.read()
	# string = inp.split(" ")
	# email = string[0]
	# ticker = string[1]
	# new_quantity = string[2]


	loc = DBFile #must be an xlsx file

	#open database file
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 
	sheet.cell_value(0, 0)

	num = sheet.nrows

	#initialize lists
	emails = []
	tickers = []
	prices = []
	quants = []

	i = 1


	#get data currently in db, and update quantity for matching ticker/email combination
	while i < num:
		if sheet.cell_value(i, 0) != email or sheet.cell_value(i, 1) != ticker:
			emails.append(sheet.cell_value(i, 0))
			tickers.append(sheet.cell_value(i, 1))
			prices.append(sheet.cell_value(i, 2))
			quants.append(sheet.cell_value(i, 3))
		else:
			emails.append(sheet.cell_value(i, 0))
			tickers.append(sheet.cell_value(i, 1))
			prices.append(sheet.cell_value(i, 2))
			quants.append(int(new_quantity))

		i = i + 1


	#push to DB
	df = DataFrame({'Email': emails, 'Symbol': tickers, 'Price': prices, 'Quantity': quants})
	df = df[['Email', 'Symbol', 'Price', 'Quantity']]

	df.to_excel(newDBFile, sheet_name = 'sheet1', index=False)


#Takes in email (string), ticker (string), price (float), quantity(int), DBFile (string, xlsx file path)
#and updates the DB file containing the new tuple.
def addtoDB(email, ticker, price, quantity, DBFile):
	#inp = sys.stdin.read()

	loc = DBFile #must be a .xlsx

	#open database
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 
	sheet.cell_value(0, 0)

	num = sheet.nrows

	#initialize lists
	emails = []
	tickers = []
	prices = []
	quants = []

	#example
	# emails = ['jack.roth@yale.edu', 'david.schwartz@yale.edu', 'benjamin.wang@yale.edu', 'juan.valencia@yale.edu']
	# tickers = ['AAPL', 'MSFT', 'BLK', 'GS']
	# prices = [160.9, 190.81, 480.84, 203.84]
	# quants = [4, 100, 45, 72]

	i = 1

	#get data currently in DB, minus the header row
	while i < num:
		emails.append(sheet.cell_value(i, 0))
		tickers.append(sheet.cell_value(i, 1))
		prices.append(sheet.cell_value(i, 2))
		quants.append(sheet.cell_value(i, 3))
		i = i + 1

	#if using stdin:
	# for line in inp.splitlines():
	# 	spl = line.split(" ")
	# 	emails.append(spl[0])
	# 	tickers.append(spl[1])
	# 	prices.append(float(spl[2]))
	# 	quants.append(int(spl[3]))

	#add to DB lists
	emails.append(email)
	tickers.append(ticker)
	prices.append(price)
	quants.append(quantity)

	#push to DB

	df = DataFrame({'Email': emails, 'Symbol': tickers, 'Price': prices, 'Quantity': quants})
	df = df[['Email', 'Symbol', 'Price', 'Quantity']]

	df.to_excel(loc, sheet_name = 'sheet1', index=False)







