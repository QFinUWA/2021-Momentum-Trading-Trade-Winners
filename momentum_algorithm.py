import itertools
import sys

import pandas as pd
from talib.abstract import *

# local imports
from gemini_modules import engine

# read in data preserving dates
df = pd.read_csv("data/USDT_LTC.csv", parse_dates=[0]) 

# initializes backtesting engine
backtest = engine.backtest(df)

# globals...

# lookback moving average lengths
# longterm should not be less than RSI lookback length
moving_av_lengths = { 
    'longterm'  : 35, 
    'midterm'   : 30,
    'shortterm' : 25
}

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
            midterm_moving_average = lookback['close'].rolling(window=moving_av_lengths['midterm']).mean()[today]
            longterm_moving_average = lookback['close'].rolling(window=moving_av_lengths['longterm']).mean()[today]            

            # see if longterm is low or it is high
            longterm_is_low  = (longterm_moving_average < shortterm_moving_average) and (longterm_moving_average < midterm_moving_average)
            longterm_is_high = (longterm_moving_average > shortterm_moving_average) and (longterm_moving_average > midterm_moving_average)
            
            # rsi_score = rsi(lookback)[today]

            # trading logic

            # the FIRST dip we define as the dip that we
            # entered our position at - only take action if
            # the dip we detect is a new dip
            if longterm_is_high and not IN_FIRST_DIP:
                if (not invested):
                    if (shortterm_moving_average > midterm_moving_average):
                        account.enter_position('long', account.buying_power, lookback['close'][today])
                        IN_FIRST_DIP = True

                else:                
                    for position in account.positions:
                        account.close_position(position, 1, lookback['close'][today])
                        IN_FIRST_DIP = False

            if longterm_is_low:
                IN_FIRST_DIP = False

    except Exception as e:
        print(e)

# ------------------------------------[TESTING CODE BELOW]--------------------------------------------------------------------


'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def kanes_stuff(account, lookback):
    try:
        # sets today to the index of the current day
        today = len(lookback)-1

        # skips the data until it has enough to look back on 
        if(today > training_period): 
            # takes today's price and volumn moving average
            price_moving_average = lookback['close'].rolling(window=training_period).mean()[today]  # update PMA
            volumn_moving_average = lookback['volume'].rolling(window=training_period).mean()[today]  # update VMA

            if(lookback['close'][today] < price_moving_average):
                if(lookback['volume'][today] > volumn_moving_average):

                    # if the spare money to buy exists
                    if(account.buying_power > 0):
                        
                        # spend all your money on buying
                        account.enter_position('long', account.buying_power, lookback['close'][today])
                        
            elif(lookback['close'][today] > price_moving_average):
                if(lookback['volume'][today] < volumn_moving_average):
                    
                    # sell all investments
                    for position in account.positions:
                            account.close_position(position, 1, lookback['close'][today]) 

    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset

# mass testing function
# if __name__ == "__main__":

#     # define range to sweep
#     vals = range(5, 55, 5)

#     # force print to a txt file
#     orig_stdout = sys.stdout
#     with open("test.txt", "w") as f:
#         sys.stdout = f

#         # test all combinations
#         for short, mid, long in itertools.combinations(vals, 3):
            
#             # reset global 
#             moving_av_lengths = { 
#                 'longterm'  : long, 
#                 'midterm'   : mid,
#                 'shortterm' : short
#             }
            
#             print(f'\n\n({short}, {mid}, {long})\n')
#             backtest.start(100, logic)
#             backtest.results()
#             sys.stdout

#         sys.stdout = orig_stdout

if __name__ == "__main__":
    backtest.start(100, logic)
    backtest.results()
    backtest.chart()
