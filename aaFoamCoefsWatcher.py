#!/usr/bin/env python
# coding: utf-8

r"""Live matplotlib plot of coefficients (aimed at 2D foil simulations)"""

from os import getcwd
from os.path import basename, isfile
from typing import Tuple, List, Any
import logging

import matplotlib.pyplot as plt
import matplotlib.animation as animation

logger = logging.getLogger(__name__)

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) \
    = plt.subplots(2, 3, sharex='col')

axs = [ax1, ax2, ax3, ax4, ax5, ax6]


def _line2values(line: str) -> Tuple[float, ...]:
    r"""Convert a line of a coefficient.dat file to numeric values

    Parameters
    ----------
    line : line from coefficient.dat file

    """
    tokens_unprocessed = line.split()
    tokens = [x.replace(")", "").replace("(", "") for x in tokens_unprocessed]
    floats = [float(x) for x in tokens]
    time, Cd, Cs, Cl, CmRoll, CmPitch, CmYaw, Cd_f, Cd_r, Cs_f, Cs_r, Cl_f, Cl_r = \
        floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], \
        floats[6], floats[7], floats[8], floats[9], floats[10], floats[11], floats[12]

    return time, Cd, Cs, Cl, CmRoll, CmPitch, CmYaw, Cd_f, Cd_r, Cs_f, Cs_r, Cl_f, Cl_r


def animate(frame: int, *fargs: List[Any]) -> None:
    r"""Function for the matplotlib animation.FuncAnimation call"""
    times, Cds, Css, Cls, CmRolls, CmPitchs, CmYaws, Cd_fs, Cd_rs, Cs_fs, Cs_rs, Cl_fs, Cl_rs = \
        [], [], [], [], [], [], [], [], [], [], [], [], []

    coef_file = fargs[0]
    plot_last = fargs[1]
    precision = fargs[2]

    if not isfile(coef_file):
        raise IOError("Could not find a coefficients file")

    with open(coef_file) as fd:
        for line in fd:
            if line[0] == "#":
                continue
            time, Cd, Cs, Cl, CmRoll, CmPitch, CmYaw, Cd_f, Cd_r, Cs_f, Cs_r, Cl_f, Cl_r = \
                _line2values(line)
            times.append(time)
            Cls.append(Cl)
            Cds.append(Cd)
            Css.append(Cs)  # Side force (i.e. Z up or down in XY 2D foil case)
            CmRolls.append(CmRoll)
            CmPitchs.append(CmPitch)
            CmYaws.append(CmYaw)

            ys = [Cls, Cds, Css, CmRolls, CmPitchs, CmYaws]
            titles = ['Cl', 'Cd', 'Cs', 'Cm Roll', 'Cm Pitch', 'Cm Yaw']

    plt.suptitle("%s | averages and ranges on last %d timesteps" % (basename(getcwd()), plot_last), fontsize=10)

    for ax, y, title in zip(axs, ys, titles):
        ax.clear()
        ax.set_title("%s (%s)" % (title, str(round(sum(y[-plot_last:-1]) / len(y[-plot_last:-1]), precision))))
        ax.set_ylim(min(y[-plot_last:-1])-0.0001, max(y[-plot_last:-1])+0.0001)
        ax.plot(times, y)
        ax.grid()


if __name__ == "__main__":
    from argparse import ArgumentParser

    logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="Live graphs of coefficients")
    parser.add_argument("coef_file", help="Path to the coefficient.dat file")
    parser.add_argument('-l', '--last',
                        type=int,
                        default=100,
                        help="Range of plot based on last n measurement")
    parser.add_argument('-r', '--refresh',
                        type=int,
                        default=1,
                        help="Refresh frequency in seconds")
    parser.add_argument('-p', '--precision',
                        type=int,
                        default=4,
                        help="Number of decimal digits")

    args = parser.parse_args()
    ani = animation.FuncAnimation(fig, animate,
                                  fargs=[args.coef_file, args.last, args.precision],
                                  interval=args.refresh * 1000)
    plt.show()
