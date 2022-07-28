import pandas as pd
from matplotlib import pyplot as plt
import os
import sunpy.map
from aiapy.calibrate.prep import register as aiaprep  # sunpy.instr.aia.aiaprep was moved to aiapy
from sunpy.net import Fido, attrs as a
from astropy import units as u
import datetime
import glob
import numpy as np

from matplotlib.backends.backend_pdf import PdfPages


import warnings
warnings.filterwarnings("ignore")

# read from excelsheet called Test1
df = pd.read_excel('./IRIS_AIA.xlsx' , sheet_name='Test1')

folder = '/Users/delbe/OneDrive - FHNW/aia_data/'

with PdfPages('test3.pdf') as pdf:

    for label, row in df.iterrows():
        p1_x1 = row[1]
        p1_y1 = row[2]
        p2_x2 = row[3]
        p2_y2 = row[4]

        gradient = (p2_y2-p1_y1)/(p2_x2-p1_x1)
        origin =p1_y1 - gradient * p1_x1

        y = np.arange(min(p1_y1, p2_y2),max(p1_y1, p2_y2)+1)
        x = (y - origin) / gradient

        coords = (np.column_stack((x.round().astype(int),y.astype(int))))

        final_image = []

        list_dates = []

        files = glob.glob(folder + row[0] + "/*")

        for i in range(0,len(files)-1):

            if i%10 == 0:
                print(i, end=',')

            try:
                aia1 = sunpy.map.Map(files[i])

            except:
                continue

            aia = aiaprep(aia1)

            spilltet_date = aia.date.isot.split("T")

            list_dates.append(spilltet_date[1])

            zi = np.flipud(aia.data.T)[coords[:,1], coords[:,0]]

            if len(final_image) == 0:
                final_image = zi
            else:
                final_image = np.vstack([final_image, zi])


        fig, ax = plt.subplots(figsize=[30,10])

        plt.title(row[0])

        nticks =20
        ax.xaxis.set_major_locator(MaxNLocator(nticks))
        ax.set_xticklabels(list_dates[::int(len(list_dates)/nticks)], rotation = 50, horizontalalignment="right")

        im = plt.imshow(final_image.transpose(),cmap = aia.cmap, origin = "lower", aspect="auto")  # Please adapt the axes for the correct annotation (y-solar coordinates and x-time)
        plt.colorbar()


        plt.xlabel('Time')
        plt.ylabel('Position')
        
        # save the data as numpy array ".npy" in the folder aia_data
        np.save(f"aia_data/{row[0]}" , final_image)

        plt.show()
        pdf.savefig(fig)
        plt.close()
        
print("Done")
