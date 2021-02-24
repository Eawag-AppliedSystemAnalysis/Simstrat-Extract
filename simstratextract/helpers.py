from os import path, listdir
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def results_files(dir):
    files = listdir(dir)
    out_files = []
    for file in files:
        if "_out.dat" in file:
            out_files.append(file)
    return out_files


def simstrat_time_to_datetime(days, reference_date):
    return reference_date + timedelta(days=days)


def read_file(file, reference_date):
    df = pd.read_csv(file)
    df["time"] = df.iloc[:, 0].apply(lambda x: simstrat_time_to_datetime(x, reference_date))
    df = df.set_index('time', drop=True)
    df = df.drop(df.columns[0], axis=1)
    start = min(df.index)
    end = max(df.index)
    return start, end, df
