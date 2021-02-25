import os
from simstratextract import SimstratExtract
folder = "Q:\Messdaten\Simstrat\Simstrat"
files = os.listdir(folder)
simulations = []
for file in files:
    if "." not in file:
        simulations.append(os.path.join(folder, file))
params = ["T"]

#simulations = ["/media/jamesrunnalls/JamesSSD/Eawag/Simstrat/git/Simstrat-Operational/Simulation/Soppensee","/media/jamesrunnalls/JamesSSD/Eawag/Simstrat/git/Simstrat-Operational/Simulation/LakeGeneva"]

se = SimstratExtract()
se.read_dirs(simulations, params)
se.extract_surface_parameter("T", "../data/test")
