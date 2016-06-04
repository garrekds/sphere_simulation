"""
Plotting for one-dimensional point movement simulation.
Author: Garrek Stemo


Plots position over time of two particles in point_sim.py.
Use pos_data.csv file.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


csvfile = sys.argv[1]  #csv file path.


df = pd.read_csv(csvfile)
df.plot()
plt.show()
