#!/usr/bin/python3

import pandas as pd
import editDB as db
from pandas_datareader import data

import matplotlib

import datetime
from sklearn import linear_model
import numpy as np

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt


# Takes in email and returns a dataframe with the portfolio value over the last
# 5 years. Also includes a column 'initial' for initial value of portfolio, and
# 'market' for market performance (using SPY)
# format of returned df: (Date, value, initial, market)
def getPortfolioValue(email, DBFile):
	holdings = db.getFromDB(email, DBFile)
	boughtat = sum(holdings['Price'] * holdings['Quantity']) # initial value of portfolio
	tickers = list(holdings['Symbol'])
	quants = holdings[['Symbol', 'Quantity']]

	prices = getData(tickers)
	prices = prices.merge(quants, on='Symbol')

	prices['value'] = prices['price'] * prices['Quantity']
	value = prices[['Date', 'value']]	
	value = value.groupby('Date').sum().reset_index()

	value['initial'] = boughtat

	market = getData('SPY')
	value = value.merge(market[['Date', 'price']], on='Date')
	value = value.rename(index=str, columns={'price':'market'})

	return value

def getPortfolioComponents(email, DBFile):
	holdings = db.getFromDB(email, DBFile)

	prices = getData(list(holdings.Symbol))
	latestdate = prices.Date.iloc[-1]
	currPrices = prices[prices['Date'] == latestdate]

	holdings = holdings.merge(currPrices[['Symbol', 'price']], on='Symbol')
	holdings = holdings.rename(index=str, columns={'Price':'Buy Price', 'price':'Current Price'})
	holdings['Buy Value'] = holdings['Buy Price'] * holdings['Quantity']
	holdings['Current Value'] = holdings['Current Price'] * holdings['Quantity']
	holdings = holdings[['Symbol', 'Quantity', 'Buy Price','Buy Value', 'Current Price', 'Current Value']]
	return holdings

# calls API to get the data for the selected tickers. Returns a df in the
# following format: columns are (Date, Symbol, price). Date goes back 5 years.
# if it is a single ticker it is (Date, price, Symbol)
def getData(tickers):
	ed = datetime.datetime.now().date()
	end = str(ed)
	td = datetime.timedelta(days=5*365)
	start = str(ed - td)

	# tickers = tuple(tickers)
	if not isinstance(tickers, str):
		if len(tickers) == 1:
			tickers = tickers[0]
		else:
			tickers = list(set(tickers))

	df = data.DataReader(tickers, 'iex', start, end)

	df = df.loc[:,'close']

	# single ticker
	if isinstance(tickers, str):
		df = df.reset_index()
		df['Symbols'] = tickers
		df = df.rename(index=str, columns={'date':'Date', 'Symbols':'Symbol', 'close':'price'} )
		return df

	# multiple tickers
	df = df.stack().reset_index()
	df = df.rename(index=str, columns={'date':'Date', 'Symbols':'Symbol', 0:'price'})
	return df

# using the dataframe given by getPortfolioValues(), produces a PNG
# of the plot which can then be embedded in html
def producePNG(values, filename):
	fig, ax= plt.subplots(figsize=(16,9))

	pf = pd.DataFrame(values.value.values, index=values.Date)
	pf.index = pd.to_datetime(pf.index)

	init = pd.DataFrame(values.initial.values)
	init.index = pf.index

	mkt = pd.DataFrame(values.market.values)
	mkt.index = init.index
	mkt = mkt * values.value[0]/values.market[0] 

	ax.plot(init, label='Purchase Price', color='red')
	ax.plot(pf, label='Portfolio')
	ax.plot(mkt, label='Market', color='green')

	ax.set_xlabel('Date')
	ax.set_ylabel('Equity ($)')	

	ax.legend()

	ax.set_title('Portfolio Value')

	# fig.show()

	if filename != None:
		plt.savefig(filename)

# plots without saving
def plotGraph(values):
	producePNG(values, None)


# returns a dictionary with key stats for the given data
# input: values array with format (Date, value, market)
# output: dictionary containing
# 'hwm': high water mark
# 'maxDD': max drawdown, in percentage points
# 'currentDD': current drawdown, in percentage points
# 'CAGR': CAGR, in percentage points
# 'alpha': alpha over market
# 'beta': beta to market
# 'maxDailyLoss': max daily loss, in percentage points
def getStats(values):
	results = {}
	# values is a timeseries 
	# should have 'value', 'Date' columns
	# should also have 'market' column
	workingvalues = values.copy()
	workingvalues['hwm'] = workingvalues.value.expanding().max()
	workingvalues['dd'] = 1 - workingvalues.value/workingvalues.hwm
	cagr = (workingvalues.value.iloc[-1]/workingvalues.value[0]) ** 0.2 - 1
	workingvalues['loss'] = workingvalues.value.diff().shift(-1)
	workingvalues['loss'] = workingvalues.loss/workingvalues.value
	maxDailyLoss = min(workingvalues.loss) * (-1)

	results['High-water Mark'] = workingvalues.hwm.iloc[-1]
	results['Max Drawdown'] = max(workingvalues.dd) * 100
	results['Current Drawdown'] = workingvalues.dd.iloc[-1] * 100
	results['CAGR'] = cagr * 100
	results['Maximum Daily Loss'] = maxDailyLoss * 100

	workingvalues['pfrets'] = (workingvalues.value.shift(-1)/workingvalues.value) - 1
	workingvalues['marketrets'] = (workingvalues.market.shift(-1)/workingvalues.market) - 1

	lm = linear_model.LinearRegression()

	y = workingvalues.pfrets[~np.isnan(workingvalues.pfrets)]
	X = workingvalues.marketrets[~np.isnan(workingvalues.marketrets)]

	model = lm.fit(X.values.reshape(-1,1), y)

	results['Alpha'] = model.intercept_
	results['Beta'] = model.coef_[0]

	results = pd.DataFrame.from_dict(results, orient='index')
	results = results.rename(index=str, columns={0:'Value'})
	results.Value = np.round(results.Value, decimals=5)
	return results

def main():
	data = getPortfolioValue('david.schwartz@yale.edu', 'test.xlsx')
	stats = getStats(data)
	producePNG(data, 'myportfolioplot.png')

if __name__ == "__main__":
	main()