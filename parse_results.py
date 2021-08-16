import pandas as pd

df = pd.DataFrame(columns=list(['window sizes', 'profit']))

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
            print(line)

        if 'Strategy' in line:

            profit = float(line[15:19])

            print(profit)

            df = df.append({'window sizes':tuple, 'profit':profit}, ignore_index=True)

df.to_csv('results.txt')
