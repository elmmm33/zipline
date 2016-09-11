import sys
import numpy as np
import pandas as pd
import talib
from zipline.api import *
from zipline.api import symbol
from zipline.utils.factory import load_from_yahoo
from zipline.algorithm import TradingAlgorithm
from datetime import datetime, date
import csv


def initialize(context):
	context.sym = symbol('AAPL')
	context.i = 0
	context.signal = False
	buy_order = []
	sale_order = [] #decide whether two sma cross

def handle_data(context, data):

	context.i += 1
	if context.i < 30: # skip first 30 day to get enough windows
		return

	#caculate sma
	short_dt = data.history(context.sym, 'price', 10, '1d').values
	long_dt = data.history(context.sym, 'price', 30, '1d').values
	#print short_dt
	short_sma = talib.SMA(short_dt, 10)[-1]
	long_sma = talib.SMA(long_dt, 30)[-1]
	#print 	short_sma, long_sma

	#today = data.history(context.sym, 'price', 1, '1d') #today price
	today = data.current(context.sym, 'price')

	if (short_sma > long_sma) and (context.signal is False):
		context.signal = True
		buy_order = order_percent(context.sym, 0.5) # making trade order with 50%


	elif (short_sma < long_sma) and (context.signal is True):
		context.signal = False
		sale_order = order_percent(context.sym, 0) # saling


###
######

assets = ['AAPL']
start_date = datetime.strptime('2014-01-01', '%Y-%m-%d')
end_date = datetime.strptime('2014-12-31', '%Y-%m-%d')
data = load_from_yahoo(stocks=assets, start=start_date, end=end_date)
#print data
#data = data.dropna()

algo = TradingAlgorithm(
		initialize = initialize,
		handle_data = handle_data,
		)

results = algo.run(data)
#print results.tail()
results.to_csv('output.csv')











