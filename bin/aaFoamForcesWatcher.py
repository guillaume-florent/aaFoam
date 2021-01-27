#!/usr/bin/env python
# coding: utf-8

r"""Live matplotlib plot of OpenFOAM computed forces"""

import sys
from os import getcwd
from os.path import basename, isfile
from typing import Tuple, List, Any
import logging
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from aa_foam.forces import force_data

logger = logging.getLogger(__name__)

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) \
    = plt.subplots(3, 3, sharex='col')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]


def checks(timestep: int) -> Tuple[bool, str]:
    r"""Check the existence of a suitable forces file"""
    if isfile(f"postProcessing/forces/{timestep}/force.dat"):
        return True, f"Found force file at postProcessing/forces/{timestep}/force.dat\nThe force file is in NEW format"
    elif isfile(f"postProcessing/forces/{timestep}/forces.dat"):
        return True, f"Found force file at postProcessing/forces/{timestep}/forces.dat\nThe force file is in OLD format"
    else:
        return False, "ERROR : Could not find a forces file"


def animate(frame: int, *fargs: List[Any]) -> None:
    r"""Function for the matplotlib animation.FuncAnimation call"""
    timestep = fargs[0]
    plot_last: int = fargs[1]
    precision: int = fargs[2]

    if isfile(f"postProcessing/forces/{timestep}/force.dat"):
        filename_force = f"postProcessing/forces/{timestep}/force.dat"
        old_format = False
    elif isfile(f"postProcessing/forces/{timestep}/forces.dat"):
        filename_force = f"postProcessing/forces/{timestep}/forces.dat"
        old_format = True
    else:
        # Should never happen as this has been checked before launching the animate loop
        raise IOError("Could not find a forces file")

    times, ys, titles, avgs = force_data(filename_force, old_format, avg_last=plot_last)

    colors = {'x': "red", 'y': "green", 'z': "blue"}

    plt.suptitle(f"{basename(getcwd())} | averages and ranges on last {plot_last} timesteps", fontsize=10)

    for ax, y, title in zip(axs, ys, titles):
        ax.clear()
        ax.set_title(f"{title} ({str(round(avgs[title], precision))})")
        ax.set_ylim(min(y[-plot_last:-1])-0.0001, max(y[-plot_last:-1])+0.0001)
        # Convention : 4th letter of title must be x, y or z and determines the colour.
        ax.plot(times, y, color=colors[title[3]])
        ax.grid()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="Live graphs of forces")
    parser.add_argument('-l', '--last',
                        type=int,
                        default=100,
                        help="Range of plot based on last n measurement")
    parser.add_argument('-t', '--timestep',
                        type=int,
                        default=0,
                        help="Timestep subfolder name where the force.dat lives in the postProcessing folder")
    parser.add_argument('-r', '--refresh',
                        type=int,
                        default=1,
                        help="Refresh frequency in seconds")
    parser.add_argument('-p', '--precision',
                        type=int,
                        default=4,
                        help="Number of decimal digits")

    args = parser.parse_args()
    file_ok, msg = checks(args.timestep)  # so that logging messages are not in the animate loop
    print(msg)
    if file_ok is True:
        ani = animation.FuncAnimation(fig, animate,
                                      fargs=[args.timestep, args.last, args.precision],
                                      interval=args.refresh * 1000)
        plt.show()
    else:
        sys.exit(1)
