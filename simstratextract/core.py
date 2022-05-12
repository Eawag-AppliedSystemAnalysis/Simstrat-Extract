# -*- coding: utf-8 -*-
from . import helpers
from os import path, listdir
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import simplejson as json


class SimstratExtract:
    def __init__(self):
        self.data = {}
        self.reference_date = datetime(1981, 1, 1)
        self.max_date = datetime.now()
        self.min_date = self.reference_date
        self.parameter_dict = {"Amsoldingersee": 36,
                               "Daubensee": 47,
                               "Greifensee": 3,
                               "Huttwilersee": 11,
                               "Inkwilersee": 54,
                               "Klontalersee": 20,
                               "LacdeJoux": 17,
                               "LacdelaGruyere": 19,
                               "LacdelHongrin": 32,
                               "LacNoir": 50,
                               "LagodiPoschiavo": 51,
                               "LagodiVogorno": 13,
                               "LagoRitom": 21,
                               "LakeAegeri": 6,
                               "LakeBaldegg": 7,
                               "LakeBiel": 2,
                               "LakeBrienz": 12,
                               "LakeCadagno": 15,
                               "LakeDavos": 49,
                               "LakeGeneva": 1,
                               "LakeHallwil": 8,
                               "LakeLauerz": 44,
                               "LakeLucerne-Alpnachersee": 30,
                               "LakeLucerne-Gersauer-andTreibbecken": 34,
                               "LakeLucerne-KreuztrichterandVitznauerbecken": 37,
                               "LakeLucerne-Urnersee": 31,
                               "LakeLungern": 25,
                               "LakeMaggiore": 14,
                               "LakeMurten": 26,
                               "LakeNeuchatel": 27,
                               "LakePfaffikon": 28,
                               "LakeSarnen": 29,
                               "LakeSempach": 23,
                               "LakeSils": 38,
                               "LakeSilvaplana": 40,
                               "LakeStMoritz": 41,
                               "LakeThun": 16,
                               "LakeZug": 39,
                               "LejdaVadret": 48,
                               "LowerLakeConstance": 53,
                               "LowerLakeLugano": 24,
                               "LowerLakeZurich": 5,
                               "Mauensee": 55,
                               "Moossee": 52,
                               "Oeschinensee": 9,
                               "Rotsee": 45,
                               "Sihlsee": 42,
                               "Soppensee": 18,
                               "Turlersee": 33,
                               "UpperLakeConstance": 10,
                               "UpperLakeLugano": 22,
                               "UpperLakeZurich": 4,
                               "Wagitalersee": 43,
                               "Walensee": 35,
                               "Husemersee": 152,
                               "Huttnersee": 145,
                               "Lutzelsee": 57,
                               "Mettmenhaslisee": 148,
                               "Egelsee": 147,
                               "UntererChatzensee": 150,
                               "Seeweidsee": 154,
                               }
        print("Initialised Simstrat Extract Object")

    def set_reference_date(self, dt):
        self.refernce_date = dt

    def read_dirs(self, dirs, params):
        for dir in dirs:
            if not path.isdir(dir):
                raise Exception("The directory {} does not exist.".format(dir))
            results_dir = path.join(dir, "Results")
            if not path.isdir(results_dir):
                raise Exception("The directory {} does not contain a results folder.".format(dir))
            sim_name = path.basename(dir)
            self.data[sim_name] = {}
            files = helpers.results_files(results_dir)
            for file in files:
                if file.split("_")[0] in params:
                    start, end, df = helpers.read_file(path.join(results_dir, file), self.reference_date)
                    self.data[sim_name][file.split("_")[0]] = df
                    self.min_date = min(self.min_date, start)
                    self.max_date = max(self.max_date, end)

    def extract_parameter(self, param, out_folder, round=2):
        delta = self.max_date - self.min_date
        base = self.min_date.replace(hour=0, minute=0, second=0, microsecond=0)
        arr = np.array([base + timedelta(days=i) for i in range(delta.days)])
        df = pd.DataFrame(arr)
        df.columns = ["time"]
        df = df.set_index("time", drop=True)
        for key in self.data:
            if param in self.data[key]:
                df_data = self.data[key][param].resample('D').mean().iloc[:, [1, -1]]
                df_data.columns = [key + "_bottom", key + "_surface"]
                df_data[key + "_bottom"] = df_data[key + "_bottom"].round(round)
                df_data[key + "_surface"] = df_data[key + "_surface"].round(round)
                df = df.merge(df_data, left_index=True, right_index=True, how="left")

        df = df.dropna(how='all')
        columns = df.columns
        df["unix"] = df.index.astype(int) / 10**9
        start_year = self.min_date.year
        end = datetime.fromtimestamp(df["unix"].max())
        end_year = end.year

        for year in range(start_year, end_year + 1):
            df_year = df.loc[datetime(year, 1, 1):datetime(year, 12, 31)]
            out = {"time": list(df_year["unix"])}
            for col in columns:
                arr = col.split("_")
                if not df_year[col].isnull().all():
                    if arr[0] in self.parameter_dict:
                        if self.parameter_dict[arr[0]] not in out:
                            out[self.parameter_dict[arr[0]]] = {}
                        out[self.parameter_dict[arr[0]]][arr[1]] = list(df_year[col])
            outfile = path.join(out_folder, param + "_" + str(year) + "0101_" + str(min(int(str(year) + "1231"), int(end.strftime("%Y%m%d")))) + ".json")
            with open(outfile, 'w') as f:
                json.dump(out, f, ignore_nan=True)

