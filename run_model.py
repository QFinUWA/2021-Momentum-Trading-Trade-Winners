from multiprocessing import Pool
import psutil
from os import scandir

from tqdm import tqdm

from random import randint
import pandas as pd

from contextlib import redirect_stdout

# imports to run momentum algorithm
from talib.abstract import *
from gemini_modules import engine

# momentum algorithm
from momentum_algorithm import logic, rsi

scales = {
	'half hourly': 1,
	'hourly': 2,
	'4 hourly': 8,
	'8 hourly': 16,
	'12 hourly': 24,
	'daily': 48,
	'3 daily': 144,
	'weekly': 336,
}
scale =  'half hourly'
moving_av_lengths = { 
	'shortterm' : 9*scales[scale],   
	'midterm'   : 20*scales[scale],
	'longterm'  : 30*scales[scale]
}

RSI_LOW = 30
RSI_HIGH = 70

FEE = 0.002

# Flags
IN_FIRST_DIP = False

# DAYS IN A TRADING MONTH for RSI parameter
RSI_HISTORY = 24

def simulate_once(coinname,df,lowrange,highrange):
	# define range to sweep

	DATADUMP = "datadump"
	# b.to_csv(f"{DATADUMP}/{coinnname}-{lowrange}-{highrange}")

	# initializes backtesting engine
	backtest = engine.backtest(df)

	backtest.start(100, logic)
	with open(f'datadump/{coinname}.txt', 'a') as f:
		with redirect_stdout(f):
			backtest.results()

def run_simulation():
	# initialize constants
	trainingperiod = 500
	samplesize = 5

	# initialize directory
	DATADIR = "datatest"
	TESTDIR = "test_data"
	TRAINDIR = "train_data"

	# gather training data files
	trainingfiles = [i.path for i in scandir(TRAINDIR) if i.is_file()]

	# determine cpu count and initialize a pool
	# iterate through training files
	num_cpus = psutil.cpu_count(logical=False)
	with Pool(num_cpus) as threadpool:
		for progress, trainingfile in zip(tqdm(range(len(trainingfiles))), trainingfiles):
			coinname = trainingfile.split("/")[-1].split(".")[0]
			coindata = pd.read_csv(trainingfile)

			datapoints = coindata.shape[0]
			datarange = datapoints - trainingperiod

			offsets = [randint(0, datarange+1) for i in range(samplesize)]
			ranges = [(offset, offset+trainingperiod) for offset in offsets]

			datasets = [coindata.iloc[r[0] : r[1]] for r in ranges]

			# in the form (coin name, reduced df, lower bound, upper bound)
			args = [
				(coinname, data, r[0], r[1])
				for data, r in zip(datasets, ranges)
			]

			# run the pool with the necessary arguments
			threadpool.starmap(simulate_once, args)



def main():
	run_simulation()

if __name__ == '__main__':
	main()