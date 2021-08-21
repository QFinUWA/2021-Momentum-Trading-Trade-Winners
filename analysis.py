# Example raw output
'''
###################### START ######################
1  (short)
2  (mid)
4  (long)
24 (rsi history)
-------------- Results ----------------

Buy and Hold : 197.62%
Net Profit   : 197.62
Strategy     : -23.65%
Net Profit   : -23.65
Longs        : 1307
Sells        : 1307
Shorts       : 0
Covers       : 0
--------------------
Total Trades : 2614

---------------------------------------
###################### END ######################
'''

# Example parsed input
'''
short
mid
long
rsi (history)
buy and hold
net profit
strategy
net profit
longs
sells
shorts
covers
'''

from sys import argv

class DataObject:
	DATAPOINTS = 13

	INPUT_SCHEMA = [
		"short",
		"mid",
		"long",
		"rsi_history",
		"buy_and_hold%",
		"buy_and_hold$",
		"strategy%",
		"strategy$",
		"longs",
		"sells",
		"shorts",
		"covers"
	]

	OUTPUT_SCHEMA = [
		"short",
		"mid",
		"long",
		"rsi_history",
		"profit",
		"profit_ratio",
		"longs",
		"sells"
	]

	def __init__(self, arr, index):
		start_index = index * 13
		end_index = start_index + 13
		object_data = arr[start_index : end_index]

		print(index, start_index, end_index)

		def parse_numeric(string):
			string = string.strip("%")
			try:
				return int(string)
			except ValueError:
				return float(string)

		object_data = list(map(parse_numeric, object_data))
		data_map = dict(zip(self.INPUT_SCHEMA, object_data))

		# print(self.INPUT_SCHEMA, arr)

		print(data_map)

		self.short				= data_map["short"]
		self.mid 				= data_map["mid"]
		self.long 				= data_map["long"]
		self.rsi_history 		= data_map["rsi_history"]
		self.buy_hold_profit 	= data_map["buy_and_hold%"]
		self.profit 			= data_map["strategy%"]
		self.longs 				= data_map["longs"]
		self.sells 				= data_map["sells"]

		self.profit_ratio = \
			(self.profit - self.buy_hold_profit) / self.buy_hold_profit

	def extract_data(obj):
		output_data = [
			obj.short,
			obj.mid,
			obj.long,
			obj.rsi_history,
			obj.profit,
			obj.profit_ratio,
			obj.longs,
			obj.sells
		]

		return dict(zip(obj.OUTPUT_SCHEMA, output_data))

def generate_data_objects(FILEPATH):
	with open(FILEPATH, 'r') as file:
		lines = [line.strip() for line in file.readlines()]

	num_samples = len(lines)//DataObject.DATAPOINTS - 1

	samples = []
	for i in range(num_samples):
		samples.append(DataObject(lines, num_samples))

	samples = sorted(
		samples,
		key=lambda x: -x.profit_ratio
	)

	samples = list(map(lambda x: x.profit_ratio, samples))
	print(samples)

def main():
	FILEPATH=argv[1]
	generate_data_objects(FILEPATH)

if __name__ == '__main__':
	main()