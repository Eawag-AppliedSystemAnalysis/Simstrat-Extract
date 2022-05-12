import os
from simstratextract import SimstratExtract
import concurrent.futures
import logging
import threading
import boto3
from datetime import datetime
import requests

folder = "/home/jamesr/Simstrat/Simulation"
files = os.listdir(folder)
simulations = []
for file in files:
    if "." not in file:
        simulations.append(os.path.join(folder, file))
params = ["T"]

se = SimstratExtract()
se.read_dirs(simulations, params)
se.extract_parameter("T", "data/temperature")

s3 = boto3.resource('s3')
bucket = s3.Bucket('eawag-simstrat')
today = datetime.today()
s3_files = [b.key for b in bucket.objects.all()]
folder = "/home/jamesr/Simstrat/Simstrat-Extract/data/temperature"
files = os.listdir(folder)
for b in s3_files:
    if str(today.year) in b:
        s3.Object('eawag-simstrat', b).delete()
for f in files:
    file = "temperature/" + f
    if file not in s3_files:
        s3.meta.client.upload_file(os.path.join(folder, f), 'eawag-simstrat', file)
requests.get("http://api.datalakes-eawag.ch/externaldata/sync/simstrat")
