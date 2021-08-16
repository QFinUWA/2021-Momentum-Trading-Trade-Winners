import pandas as pd

df = pd.DataFrame(columns=list(['window sizes', 'profit', 'trades']))

# INTRUCTIONS - using the mass testing script produces results.txt,
# change this to 'parse.txt' (So you don't accidentally override the output 
# if you run the scipt again)
with open('parse.txt', 'r') as f:

    lines = f.readlines()

    tuple = ''
    profit = 0.0

    for line in lines:
        if '(' in line:
            tuple = line[1:-2]

        if 'Strategy' in line:

            profit = float(line[15:-1])      

        if 'Sells' in line:

            trades = line[15:-1]

            df = df.append({'window sizes':tuple, 'profit':profit, 'trades': trades}, ignore_index=True)

# string = 'Sells        : 349'
# print(string[15:-2])
df.to_csv('results.csv')
