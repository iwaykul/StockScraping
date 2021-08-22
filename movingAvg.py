import time

b = []
c = []
d = []
e = []

for i in range(0, 100): 
	b.append(i+1)
for i in range(0, 1000): 
	c.append(i+1)
for i in range(0, 10000): 
	d.append(i+1)
for i in range(0, 100000): 
	e.append(i+1)

masterList = [b,c,d,e]
windows = [3,5,10,30,100]

def bruteForceMA(data, window):
	ma_list= []
	for j in range(window, len(data)): 
		movingAvg = 0
		for x in range(1,1+window): 
			movingAvg += data[x-j] 
		ma_list.append(movingAvg)
	return ma_list

def fasterWay(data, window):
	ma_list = []
	total = 0.0
	for j in range(1, 1+window): 
		total += data[j]
	movingAvg = total/window 
	ma_list.append(movingAvg)
	for i in range(1+window, len(data)):
		newMA = (total) - data[i-(1+window)] + data[i-1]
		ma_list.append(newMA/window)
	return ma_list

def test():
	for w in windows:
		before_bf = time.time()	
		bruteForceMA(e, w)	
		after_bf = time.time()
		duration_bf = (after_bf - before_bf) *1000
		string_bf  = "Time taken to brute force {} units: {} ms".format(len(e), duration_bf)
		before_fw = time.time()
		fasterWay(e, w)
		after_fw = time.time()
		duration_fw = (after_fw - before_fw) *1000
		string_fw  = "Time taken by faster way using {} units: {} ms".format(len(e), duration_fw)
		print(string_bf)
		print(string_fw)

