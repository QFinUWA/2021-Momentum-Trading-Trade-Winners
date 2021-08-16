import os

import pandas as pd

df = pd.DataFrame(columns=list(['window sizes', 'RSI bound', 'profit', 'trades']))

# INTRUCTIONS - using the mass testing script produces results.txt,
# change this to 'parse.txt' (So you don't accidentally override the output 
# if you run the scipt again)
with open('results-data/temp.txt', 'r') as f:

    lines = f.readlines()

    rolling_tuple = ''
    rsi_tuple = ''
    profit = 0.0
    trades = 0

    for line in lines:
        if '(' in line:
            rolling_tuple = line[1:-2]
        
        if '[' in line:

            rsi_tuple = line[1:-2]

        if 'Strategy' in line:

            profit = float(line[15:-2])      

        if 'Sells' in line:

            trades = int(line[15:-1])

            df = df.append({'window sizes': rolling_tuple, 'RSI bound': rsi_tuple, 'profit':profit, 'trades': trades}, ignore_index=True)

df.to_csv('results-data/results.csv')
os.remove('results-data/temp.txt')
