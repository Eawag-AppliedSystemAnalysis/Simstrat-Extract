from os import path, listdir
import pandas as pd
import numpy as np


def results_files(dir):
    files = listdir(dir)
    out_files = []
    for file in files:
        if "_out.dat" in file:
            out_files.append(file)
    return out_files


def read_file(file):
    df = pd.read_csv(file)
    depths = list(df.columns)
    del depths[0]
    depths = np.array(depths).astype(float)
    times = np.array(df.iloc[:, 0])
    df = df.drop(df.columns[0], axis=1)
    data = df.values.transpose()
    return {"depths": depths, "times": times, "data": data}
