import itertools
import os
import sys
import time
from math import comb
from multiprocessing import Process

import pandas as pd
from talib.abstract import *

# local imports
from gemini_modules import engine

# read in data preserving dates
df = pd.read_csv("data/USDT_BTC.csv", parse_dates=[0]) 

# df = df.loc['2020-02-13':]

# initializes backtesting engine
backtest = engine.backtest(df)

# globals...

# lookback moving average lengths
# longterm should not be less than RSI lookback length

# define range to sweep
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
def rsi(df, periods=RSI_HISTORY, ema=True):
    """
    Returns a pd.Series with the relative strength index.
    source: https://www.roelpeters.be/many-ways-to-calculate-the-rsi-in-python-pandas/
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi

def logic(account, lookback):
    global IN_FIRST_DIP

    try:
        # get the latest index
        today = len(lookback) -1

        # in case RSI_HISTORY > longterm lookback
        longest_lookback = max(moving_av_lengths['longterm'], RSI_HISTORY)

        # start trading after all moving averages have started
        if (today > longest_lookback):
            # our logic starts here
            invested = account.buying_power <= 0

            # get the 3 moving averages (sorry I keep forgetting my keyboard is on the mic :') )
            shortterm_moving_average = lookback['close'].rolling(window=moving_av_lengths['shortterm']).mean()[today]
            # print(shortterm_moving_average)
            # print(f'\t{today}')
            midterm_moving_average = lookback['close'].rolling(window=moving_av_lengths['midterm']).mean()[today]
            longterm_moving_average = lookback['close'].rolling(window=moving_av_lengths['longterm']).mean()[today]            

            # see if longterm is low or it is high
            longterm_is_low  = (longterm_moving_average < shortterm_moving_average) and (longterm_moving_average < midterm_moving_average)
            longterm_is_high = (longterm_moving_average > shortterm_moving_average) and (longterm_moving_average > midterm_moving_average)
            
            rsi_score = rsi(lookback)[today]
            # rsi_score = 50

            # trading logic

            # the FIRST dip we define as the dip that we
            # entered our position at - only take action if
            # the dip we detect is a new dip
            if longterm_is_high and not IN_FIRST_DIP:
                if (not invested):
                    if (shortterm_moving_average > midterm_moving_average):
                        account.buying_power = account.buying_power * (1-FEE)
                        account.enter_position('long', account.buying_power, lookback['close'][today])
                        IN_FIRST_DIP = True

                else:   
                    for position in account.positions:
                        # print("this is running")
                        account.close_position(position, 1, lookback['close'][today])
                        account.buying_power = account.buying_power * (1-FEE)
                        IN_FIRST_DIP = False
            
            # If we remove these two we actually make a more intense loss but our algorithm is much less volatile
            # In testing -removing RSI low made it better 
            
            # this just reduces volatility, seems to have a greater affect upwards rather than downwards?
            if rsi_score < RSI_LOW and not invested:
                account.buying_power = account.buying_power * (1-FEE)
                account.enter_position('long', account.buying_power, lookback['close'][today])
            
            # I'm testing just using this right now
            if rsi_score > RSI_HIGH and invested:
                for position in account.positions:
                        account.close_position(position, 1, lookback['close'][today])
                        account.buying_power = account.buying_power * (1-FEE)
                
            # dont rm
            if longterm_is_low:
                IN_FIRST_DIP = False

    except Exception as e:
        print("")
        print(e)

# ------------------------------------[TESTING CODE BELOW]--------------------------------------------------------------------

# mass testing function
# if __name__ == "__main__":

#     # define range to sweep
#     scale = 48
#     vals = range(10, 101, 10)
#     # vals = [2, 10, 20]
#     vals = list(map(lambda x: x*scale, vals))

#     # RSI
#     low_list = [28]
#     high_list = [100]

#     # force print to a txt file
#     orig_stdout = sys.stdout
#     count = 0
#     # total = comb(len(vals), 3)
#     total = comb(len(vals),3)*len(low_list)*len(high_list)

#     print(f'\nDoing {total} Backtests ...\n')
#     with open("results-data/temp.txt", "w") as f:
        
#         # test all combinations
#         for short, mid, long in itertools.combinations(vals, 3):
#             for low in low_list:
#                 for high in high_list:
#                     t0 = time.time()
#                     sys.stdout = f
                    
#                     # reset global 
#                     moving_av_lengths = { 
#                         'longterm'  : long, 
#                         'midterm'   : mid,
#                         'shortterm' : short
#                     }

#                     RSI_LOW = low
#                     RSI_HIGH = high
                    
#                     # do testing
#                     print(f'\n({short}, {mid}, {long})')
#                     print(f'\n[{low}, {high}]')
#                     backtest.start(100, logic)
#                     backtest.results()
#                     t1 = time.time()
#                     sys.stdout

#                     sys.stdout = orig_stdout
#                     count += 1
#                     print(f'Rolling Averages:\t{short}, {mid}, {long}\nRSI:\t\t\t{low}-{high}\n{int(t1-t0)} secs, ({count}/{total})\n')
#     import parse_results
#     os.system('play -nq -t alsa synth {} sine {}'.format(0.5, 440))

if __name__ == "__main__":
    backtest.start(100, logic)
    backtest.results()
    backtest.chart()
