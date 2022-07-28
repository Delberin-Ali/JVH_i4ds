import pandas as pd
from matplotlib import pyplot as plt

import sunpy.map
# sunpy.instr.aia.aiaprep was moved to aiapy
from aiapy.calibrate.prep import register as aiaprep
from sunpy.net import Fido, attrs as a
from astropy import units as u

import glob
import numpy as np

import warnings
warnings.filterwarnings("ignore")

print("Start....")
df = pd.read_excel('IRIS_AIA.xlsx', sheet_name='Tabelle2')

folder = '/Users/delbe/OneDrive - FHNW/aia_data/aia_171'

for label, row in df.iterrows():
    start_time = row[5]
    end_time = row[6]

    t = a.Time(start_time, end_time)

    result = Fido.search(t, a.Instrument("aia"), a.Wavelength(
        171*u.angstrom), a.Sample(1*u.second))
    Fido.fetch(result, path=folder)

    print("-", end=' ')
