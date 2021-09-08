from multiprocessing import Pool
import psutil # install psutil

from tqdm import tqdm # install tqdm for progress bar

import pandas as pd

# imports to run momentum algorithm
from talib.abstract import *
from gemini_modules import engine

# momentum algorithm
from momentum_algorithm import logic


# calls logic
# capture the output if you want with backtest.results()
def logic_wrapper(arg1, arg2, arg3):
	df = ... # can take this as an arg too
	backtest = engine.backtest(df)
	backtest.start(100, logic)

def run_simulation():
	NUM_BATCHES = 10 # number of batches you want
	SIM_DATA = ["some data" for i in range(NUM_BATCHES)]
	progress_bar_iterations = tqdm(range(len(SIM_DATA)))

	# determine cpu count and initialize a pool
	num_cpus = psutil.cpu_count(logical=False)
	with Pool(num_cpus) as threadpool:
		for progress, sim in zip(progress_bar_iterations, SIM_DATA):

			# set of arguments to try with your `logic` wrapper
			args = [("arg1", "arg2", "etc")]

			# run the pool with the necessary arguments
			threadpool.starmap(logic_wrapper, args)

def main():
	run_simulation()

if __name__ == '__main__':
	main()
