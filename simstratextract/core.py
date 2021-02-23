# -*- coding: utf-8 -*-
from . import helpers
from os import path, listdir


class SimstratExtract:
    def __init__(self):
        self.data = {}
        print("Initialised Simstrat Extract Object")

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
                self.data[sim_name][file.split("_")[0]] = helpers.read_file(path.join(results_dir, file))
