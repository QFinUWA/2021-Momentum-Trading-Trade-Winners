import pandas as pd
from talib.abstract import *

# local imports
from gemini_modules import engine

# read in data preserving dates
df = pd.read_csv("data/USDT_XRP.csv", parse_dates=[0]) 

# initializes backtesting engine
backtest = engine.backtest(df)

# globals...

scales_map = {
    "daily" : 48,
    "half hourly": 1
}

scale = "daily"
scale_factor = scales_map[scale]

# lookback moving average lengths
# longterm should not be less than RSI lookback length
moving_av_lengths = { 
    'shortterm' : 9 *scale_factor,   
    'midterm'   : 14*scale_factor,
    'longterm'  : 30*scale_factor
}

# thresholds for RSI
RSI_LOW     = 35
RSI_HIGH    = 75

# Flags
IN_FIRST_DIP = False

# DAYS IN A TRADING MONTH for RSI parameter
RSI_HISTORY = 24*scale_factor
def rsi(df, periods=RSI_HISTORY):
    """
    Returns a pd.Series with the relative strength index.
    source: https://www.roelpeters.be/many-ways-to-calculate-the-rsi-in-python-pandas/
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    # Use exponential moving average
    ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        
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
            invested = account.buying_power <= 0    # we go all-in every time
                                                    # only invested when buying power = 0

            # get the 3 moving averages
            short_lookback = moving_av_lengths['shortterm']
            medium_lookback = moving_av_lengths['midterm']
            long_lookback = moving_av_lengths['longterm']

            shortterm_moving_average = lookback['close'].rolling(window=short_lookback).mean()[today]
            midterm_moving_average = lookback['close'].rolling(window=medium_lookback).mean()[today]
            longterm_moving_average = lookback['close'].rolling(window=long_lookback).mean()[today]            

            # see if longterm is low or it is high
            longterm_is_low  = (longterm_moving_average < shortterm_moving_average) and (longterm_moving_average < midterm_moving_average)
            longterm_is_high = (longterm_moving_average > shortterm_moving_average) and (longterm_moving_average > midterm_moving_average)
            

            # -------------------- trading logic --------------------

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

            # -------------------- RSI indicator -------------------- 

            rsi_score = rsi(lookback)[today]

            if RSI_LOW > rsi_score and not invested:
                account.enter_position('long', account.buying_power, lookback['close'][today])
                IN_FIRST_DIP = True
                
            if RSI_HIGH < rsi_score and invested:
                for position in account.positions:
                    account.close_position(position, 1, lookback['close'][today])
                IN_FIRST_DIP = False

            if longterm_is_low:
                IN_FIRST_DIP = False

    except Exception as e:
        print(e, "a cosmic tragedy has transpired") # git reset --hard ?

if __name__ == "__main__":
    backtest.start(100, logic)
    backtest.results()
    backtest.chart()
