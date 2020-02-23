#!/usr/bin/python3

import pandas as pd
import xlrd
from pandas import DataFrame
import sys

inp = sys.stdin.read()
string = inp.split(" ")
email = string[0]



emails = []
tickers = []
prices = []
quants = []

loc = 'test.xlsx'

df = pd.read_excel(loc, sheet_name = None)

for key in df:
	dfs = (df[key].head())


df_list = dfs.loc[dfs['Email'] == 'david.schwartz@yale.edu']

print(df_list)
