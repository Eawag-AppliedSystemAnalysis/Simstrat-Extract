# -*- coding: utf-8 -*-
from . import helpers
from os import path, listdir
from datetime import datetime, timedelta


class SimstratExtract:
    def __init__(self):
        self.data = {}
        self.reference_date = datetime(1981, 1, 1)
        self.min_date = datetime.now()
        self.max_date = self.reference_date
        print("Initialised Simstrat Extract Object")

    def set_reference_date(self, dt):
        self.refernce_date = dt

    def read_dirs(self, dirs):
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
                start, end, df = helpers.read_file(path.join(results_dir, file), self.reference_date)
                self.data[sim_name][file.split("_")[0]] = df
                self.min_date = min(self.min_date, start)
                self.max_date = max(self.max_date, end)


