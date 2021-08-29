# turns all the csv files in datatest to proper test data in datadump

import pandas as pd
from os import *

DATADIR = "datatest"
TESTDIR = "test_data"

def main():
    datafiles = [i.path for i in scandir(DATADIR) if i.is_file()]
    print(datafiles)

    for i, csv_path in enumerate(datafiles):
        coinname = csv_path.split("USD")[0].split("_")[1]

        nfiles = len(datafiles)
        print(coinname, f"{i}/{nfiles}")
        
        # needed and possible headers
        needed=f"date,open,high,low,close,volume"
        header_str=f"unix,date,symbol,open,high,low,close,volume,Volume USDT,tradecount".split(",")

        # headers to keep and remove
        header_keep=[csv_path for csv_path in header_str if csv_path in needed]
        header_remv=[csv_path for csv_path in header_str if csv_path not in needed]

        csv = pd.read_csv(csv_path)

        # remove rows
        csv = csv.drop(header_remv, axis=1)

        csv.columns = header_keep

        # format row names
        csv = csv.rename({f"Volume {coinname}" : "volume"})

        # remove 2021 data
        dates = csv.date
        dates = dates.map(lambda x: x.split("-")[0])
        dates = dates.map(lambda x: x != "2021")

        csv = csv[dates]

        # remove data not at a half hour mark
        dates = csv.date
        dates = dates.map(lambda x: x.split(":")[-2])
        dates = dates.map(lambda x: x == "30" or x == "00")

        csv = csv[dates]

        # save to a test file
        csv.to_csv(f"{TESTDIR}/{coinname}.csv")

main()