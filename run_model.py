

import numpy as np
import os
import scipy.optimize as op

import model
import utils


osarg_id = 13557



time, mag, mag_error = utils.get_light_curve(osarg_id)


import matplotlib.pyplot as plt 

fig, ax = plt.subplots()

ax.scatter(time, mag, facecolor="k")
ax.errorbar(time, mag, yerr=mag_error, fmt=None, ecolor="#666666", zorder=-1)



