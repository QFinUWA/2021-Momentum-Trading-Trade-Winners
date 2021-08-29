import pandas as pd
from os import *

DATADIR = "datatest"
DUMPDIR = "datadump"

def main():
    datafiles = [i.path for i in scandir(DATADIR) if i.is_file()]
    print(datafiles)

    for i in datafiles[:1]:
        coinname = i.split("USD")[0].split("_")[1]
        

        # needed and possible headers
        needed=f"date,open,high,low,close,volume"
        header_str=f"unix,date,symbol,open,high,low,close,volume,Volume USDT,tradecount".split(",")

        # headers to keep and remove
        header_keep=[i for i in header_str if i in needed]
        header_remv=[i for i in header_str if i not in needed]

        print(header_remv)

        csv_path = i
        csv = pd.read_csv(csv_path)

        # remove rows
        csv = csv.drop(header_remv, axis=1)

        # format row names
        csv = csv.rename({f"Volume {coinname}" : "volume"})

        # save to a test file
        csv.to_csv("datatest/TEST.csv")

        print(csv.head())




main()