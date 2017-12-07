
import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib.ticker import MaxNLocator

__all__ = ["light_curve_path", "get_light_curve", "plot_light_curve"]

def light_curve_path(osarg_id):
    """
    Return the relative system path for the file containing the OGLE light curve
    for the given OSARG identifier.

    :param osarg_id:
        The OSARG identifier from OGLE.
    """

    possible_paths = [
        "phot/I/OGLE-BLG-LPV-{osarg_id:06d}.dat",
        "phot/V/OGLE-BLG-LPV-{osarg_id:06d}.dat"
    ]
    for possible_path in possible_paths:
        path = possible_path.format(osarg_id=osarg_id)
        if os.path.exists(path):
            return path


def get_light_curve(osarg_id):
    """
    Return the OGLE light curve for an OSARG identifier.

    :param osarg_id:
        The OSARG identifier from OGLE.

    :returns:
        A three-length tuple containing the time, the stellar magnitude at each
        time, and the error on the stellar magnitude at each time.
    """
    time, mag, mag_error = np.loadtxt(light_curve_path(osarg_id)).T
    return (time, mag, mag_error)


def plot_light_curve(time, mag, mag_error, title=None, **kwargs):
    """
    Plot an OGLE light curve.

    :param time:
        The time of each observation.

    :param mag:
        The photometric magnitude at each observation time.

    :param mag_error:
        The error on the photometric magnitude at each observation time.

    :param title: [optional]
        An optional title to set to the axes.

    :returns:
        A matplotlib figure showing an OGLE light curve.
    """

    fig, ax = plt.subplots()

    ax.scatter(time, mag, facecolor="k")
    ax.errorbar(time, mag, yerr=mag_error, fmt=None, zorder=-1, ecolor="k")

    ax.xaxis.set_major_axis(MaxNLocator(6))
    ax.yaxis.set_major_axis(MaxNLocator(6))

    if title is not None:
        ax.set_title(title)

    fig.tight_layout()

    return fig