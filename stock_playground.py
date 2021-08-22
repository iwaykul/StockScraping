import requests 
from movingAvg import fasterWay
import statistics

#ticker = "SNAP"
key = "sk_b9d09441138f4dc69cd8ef61e379ac17"
watch_list = ["GOOG", "TSLA", "AAPL", "NOK", "MSFT", "GME", "MRNA", "NFLX", "BAC", "TSM"]
#url = "https://cloud.iexapis.com/stable/stock/{}/quote/latestPrice?token={}".format(ticker, key)
#print(url)
#resp = requests.get(url)
#print(resp.json())

#urlTheSecond = "https://cloud.iexapis.com/stable/stock/{}/stats?token={}".format(ticker, key)
#print(urlTheSecond)
#resp = requests.get(urlTheSecond)
#print(resp.json())

#ohlc = "https://cloud.iexapis.com/stable/stock/{}/chart/1m?token={}".format(ticker, key)
#print(ohlc)
#resp = requests.get(ohlc).json()
#window = 10

#stock/{symbol}/stats/{stat?}

def max_min_window_calculations(wind, ticker_list):
	full_tickers = []
	for t in ticker_list:
		urlTheSecond = "https://cloud.iexapis.com/stable/stock/{}/chart/3m?token={}".format(t, key)
		resp = requests.get(urlTheSecond).json()
		date_to_average = {}
		close_open = []
		date_list = []
		date_to_delta = []
		for r in resp:
			difference = r['open'] - r['close']
			close_open.append(difference)
			date_list.append(r['date'])
		calculation = fasterWay(close_open, wind) 
		for i in range(0, len(calculation)):
			date_to_delta.append((date_list[i+wind-1], calculation[i]))
		sorted_dtd = sorted(date_to_delta, key=lambda x: x[1], reverse = True)
		full_tickers.append(sorted_dtd)
	count = 0
	print("~~~~~~~~~~~~~~")
	for ticker in full_tickers:
		print("------------- {} --------------".format(count+1))
		print("Symbol: {}".format(ticker_list[count]))
		best = ticker[0]
		worst = ticker[-1]
		print("Date of Highest Positive Change: {} with a value {}".format(best[0], best[1]))
		print("Date of Highest Negative Change: {} with a value {}".format(worst[0], worst[1]))
		count = count + 1
	print("~~~~~~~~~~~~~~")

def obtainMovingAverage(w_list):
	for w in w_list: 
		ma_url = "https://cloud.iexapis.com/stable/stock/{}/stats/day50MovingAvg?token={}".format(w, key)
		response = requests.get(ma_url)
		print("{}'s 50 day moving average: {}".format(w, response.json()))
		print("-------------------------")

def currentPrice(w_list): 
	for w in w_list: 
		cp_url = "https://cloud.iexapis.com/stable/stock/{}/price?token={}".format(w, key)
		response = requests.get(cp_url)
		print("{}'s current price?: {} ".format(w, response.json()))
		print("-------------------------")


def metric(w_list):
	for w in w_list: 
		fma_url = "https://cloud.iexapis.com/stable/stock/{}/stats/day50MovingAvg?token={}".format(w, key)
		cp_url = "https://cloud.iexapis.com/stable/stock/{}/price?token={}".format(w, key)
		tma_url = "https://cloud.iexapis.com/stable/stock/{}/stats/day200MovingAvg?token={}".format(w, key)
		response_fma = requests.get(fma_url)
		response_cp = requests.get(cp_url)
		response_tma = requests.get(tma_url)
		print("{}'s 50 day moving average: {}".format(w, response_fma.json()))
		print("{}'s 200 day moving average: {}".format(w, response_tma.json()))
		print("{}'s current price?: {} ".format(w, response_cp.json()))
		greater_fma = "greater" if float(response_cp.json()) >= float(response_fma.json()) else "lesser"
		print("The current price is {} than the 50-day moving average.".format(greater_fma))
		greater_tma = "greater" if float(response_tma.json()) >= float(response_fma.json()) else "lesser"
		print("The 200-day moving average is {} than the 50-day moving average.".format(greater_tma))
		print("-----------------------------")








#max_min_window_calculations(8, watch_list)
#obtainMovingAverage(watch_list)
#for key in dta.keys():
	#print("\t {} : $ {}".format(key, round(dta[key],2)))
#currentPrice(watch_list)
metric(watch_list)

#Assuming Normal Distribution
def obtain_outliers(data, time_period): 
	mean = sum(data)/len(data) 
	std_dev = statistics.stdev(data)
	lower = max(0, mean - std_dev * 3)
	upper = mean + std_dev * 3
	#return "{} Outliers for {} are outside of : {} -> {}".format(ticker, time_period, lower, upper)
	return [lower, upper]



def collect_annual_data(time_period="1y", is_open=True): 
	important = []
	open_close_data = "https://cloud.iexapis.com/stable/stock/{}/chart/{}?token={}".format(ticker, time_period, key)
	response = requests.get(open_close_data).json()
	for r in response: 
		if (is_open): 
			important.append(r['open']) 
		else: 
			important.append(r['close'])
	return important

def obtain_price_bands(percent=20):
	pb = "https://cloud.iexapis.com/stable/stock/{}/chart/5d?token={}".format(ticker, key)
	response = requests.get(pb).json()
	yest_close = response[-1]['close']
	return [yest_close /1.2, yest_close * 1.2]


#annual_data = collect_annual_data()
#o##utliers = obtain_outliers(annual_data, "1y")
#price_bands = obtain_price_bands() 
#print(outliers)
#print("-----")
#print(price_bands)



