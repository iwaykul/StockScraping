import requests
import json 
from tkinter import *
from tkinter import messagebox

key = 'XXX'

class Application(Tk):

	def __init__(self):
		Tk.__init__(self)
		self.title("Stock Information")
		self.labelSymbol = Label(self, text= "Enter A Symbol").grid(row = 0, column = 0)
		self.stringVar = StringVar()
		self.numDays = StringVar()
		self.entrySymbol = Entry(self, textvariable=self.stringVar).grid(row = 0, column = 1)
		self.labelDay = Label(self, text= "How Many Days?").grid(row = 1, column = 0)
		self.entryDay = Entry(self, textvariable=self.numDays).grid(row = 1, column = 1)
		self.button = Button(self, text = "Obtain Info", command = self.hitButton).grid(row = 2, column = 1)
		self.symb_data = None

	def get_symbol_data(self,ticker):
		#messagebox.showinfo("Symbol Change:", ticker)
		url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
		response = requests.get(url)
		info = response.json()
		day_by_day = info['Time Series (Daily)'] 
		date_list = list(day_by_day.keys()) 
		return day_by_day, date_list


	def construct_date(self,m, d, y):
		month = str(m) if (len(str(m)) == 2) else "0" + str(m) 
		day = str(d) if (len(str(d)) == 2) else "0" + str(d)
		date_string = str(y) + "-" + str(month) + "-" + str(day)
		return date_string

	def getLastNDays(self, m, d, y, symbol, days):
		day_by_day, date_list = self.get_symbol_data(symbol)
		#messagebox.showinfo("Checkpoint", "Get Last Five Days")
		final_info = []
		date_string = self.construct_date(m,d,y) 
		i = date_list.index(date_string) 
		dates_to_search = []
		for d in range(i, i+days):
			dates_to_search.append(date_list[d])
		for d in dates_to_search: 
			daily_info = day_by_day[d]
			low = daily_info['3. low']
			high = daily_info['2. high']
			op = daily_info['1. open']
			cl = daily_info['4. close']
			final_info.append([d, low, high, op, cl])
		return final_info, symbol

	def hitButton(self): 
		try: 
			days = 5 if (self.numDays.get() == "") else int(self.numDays.get())
			last_five_data, symbol = self.getLastNDays(5,4,2021, self.stringVar.get(), days) 
			#messagebox.showinfo("Checkpoint", "Hit Button")
			self.symb_data = Tk()
			self.symb_data.title("Intro Page")
			#messagebox.showinfo("Checkpoint", "Past Title")
			t_label = Label(self.symb_data, text = symbol, bg = "lightblue").grid(row = 0, column = 3)
			d_label = Label(self.symb_data, text = "Date: ", bg = "grey").grid(row = 2, column = 0)
			h_label = Label(self.symb_data, text = "Low: ", bg = "salmon").grid(row = 2, column = 1)
			l_label = Label(self.symb_data, text = "High: ", bg = "pale green").grid(row = 2, column = 2)
			o_label = Label(self.symb_data, text = "Open: ", bg = "antique white").grid(row = 2, column = 3)
			c_label = Label(self.symb_data, text = "Close: ", bg = "antique white").grid(row = 2, column = 4)
			pc_label = Label(self.symb_data, text = "% Change: ", bg = "azure2").grid(row = 2, column = 5)

			for ix in range(0, days):	
				open_float = round(float(last_five_data[ix][3]), 2)
				close_float = round(float(last_five_data[ix][4]), 2)
				Label(self.symb_data, text = last_five_data[ix][0]).grid(row = ix+3, column = 0)
				Label(self.symb_data, text = round(float(last_five_data[ix][1]), 2)).grid(row = ix+3, column = 1)
				Label(self.symb_data, text = round(float(last_five_data[ix][2]), 2)).grid(row = ix+3, column = 2)
				Label(self.symb_data, text = open_float).grid(row = ix+3, column = 3)
				Label(self.symb_data, text = close_float).grid(row = ix+3, column = 4)
				percentChange = (open_float-close_float)*100/open_float
				percentChange = round(percentChange, 2)
				Label(self.symb_data, text = percentChange, fg= ("green2" if percentChange >= 0 else "red2")).grid(row = ix+3, column = 5)
			Button(self.symb_data, text="Close", command=self.closeDataPage).grid(row = days+3, column = 5)
			self.withdraw()
		except: 
			messagebox.showinfo("Error", "No Information Found About That Stock! Enter Another One Please")

	def testHit(self):
		messagebox.showinfo("Attention:", "Information Updated!")

	def closeDataPage(self):
		self.symb_data.withdraw()
		self.symb_data = None
		self.deiconify()



app = Application()
app.mainloop()