#!/usr/bin/env python
# coding: utf-8

r"""Live matplotlib plot of OpenFOAM computed forces"""

from os import getcwd
from os.path import basename, isfile
from typing import List, Any
import logging
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from aa_foam.forces import force_line2values, force_line2values_old_format

logger = logging.getLogger(__name__)

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) \
    = plt.subplots(3, 3, sharex='col')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]


def checks(timestep):
    r"""Check the existence of a suitable forces file"""
    if isfile("postProcessing/forces/%s/force.dat" % timestep):
        logger.info("Found force file at postProcessing/forces/%s/force.dat" % timestep)
        logger.info("The force file is in NEW format")
    elif isfile("postProcessing/forces/%s/forces.dat" % timestep):
        logger.info("Found force file at postProcessing/forces/%s/forces.dat" % timestep)
        logger.info("The force file is in OLD format")
    else:
        msg = "Could not find a forces file"
        logger.error(msg)
        raise IOError(msg)


def animate(frame: int, *fargs: List[Any]) -> None:
    r"""Function for the matplotlib animation.FuncAnimation call"""
    times, ftxs, ftys, ftzs, fpxs, fpys, fpzs, fvxs, fvys, fvzs, fpoxs, fpoys, fpozs = \
        [], [], [], [], [], [], [], [], [], [], [], [], []

    timestep = fargs[0]
    plot_last = fargs[1]
    precision = fargs[2]

    if isfile("postProcessing/forces/%s/force.dat" % timestep):
        filename_force = "postProcessing/forces/%s/force.dat" % timestep
        old_format = False
    elif isfile("postProcessing/forces/%s/forces.dat" % timestep):
        filename_force = "postProcessing/forces/%s/forces.dat" % timestep
        old_format = True
    else:
        raise IOError("Could not find a forces file")

    with open(filename_force) as fd:
        for line in fd:
            if line[0] == "#":
                continue
            if old_format is False:
                time, ftx, fty, ftz, fpx, fpy, fpz, fvx, fvy, fvz = \
                    force_line2values(line)
                times.append(time)
                ftxs.append(ftx)
                ftys.append(fty)
                ftzs.append(ftz)
                fpxs.append(fpx)
                fpys.append(fpy)
                fpzs.append(fpz)
                fvxs.append(fvx)
                fvys.append(fvy)
                fvzs.append(fvz)
                ys = [ftxs, ftys, ftzs, fpxs, fpys, fpzs, fvxs, fvys, fvzs]
                titles = ['Ft x', 'Ft y', 'Ft z', 'Fp x', 'Fp y', 'Fp z', 'Fv x', 'Fv y', 'Fv z']
            else:
                time, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, \
                    _, _, _, _, _, _, _, _, _ = force_line2values_old_format(line)
                times.append(time)
                fpxs.append(fpx)
                fpys.append(fpy)
                fpzs.append(fpz)
                fvxs.append(fvx)
                fvys.append(fvy)
                fvzs.append(fvz)
                fpoxs.append(fpox)
                fpoys.append(fpoy)
                fpozs.append(fpoz)
                ys = [fpxs, fpys, fpzs, fvxs, fvys, fvzs, fpoxs, fpoys, fpozs]
                titles = ['Fp x', 'Fp y', 'Fp z', 'Fv x', 'Fv y', 'Fv z', 'Fpoxs', 'Fpoys', 'Fpozs']

    colors = {'x': "red", 'y': "green", 'z': "blue"}

    plt.suptitle("%s | averages and ranges on last %d timesteps" % (basename(getcwd()), plot_last), fontsize=10)

    for ax, y, title in zip(axs, ys, titles):
        ax.clear()
        ax.set_title("%s (%s)" % (title, str(round(sum(y[-plot_last:-1]) / len(y[-plot_last:-1]), precision))))
        ax.set_ylim(min(y[-plot_last:-1])-0.0001, max(y[-plot_last:-1])+0.0001)
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
    checks(args.timestep)  # so that logging messages are not in the animate loop
    ani = animation.FuncAnimation(fig, animate,
                                  fargs=[args.timestep, args.last, args.precision],
                                  interval=args.refresh * 1000)
    plt.show()
