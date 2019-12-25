#!/usr/bin/env python
# coding: utf-8

r"""Live matplotlib plot of forces"""

from os import getcwd
from os.path import basename, isfile
from typing import Tuple, List, Any

import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) \
    = plt.subplots(3, 3, sharex='col')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]


def _line2values(line: str) -> Tuple[float, ...]:
    r"""Convert a line of a postProcessing/forces.dat file to numeric values

    Parameters
    ----------
    line : line from postProcessing/forces/<timestep>/force.dat

    """
    tokens_unprocessed = line.split()
    tokens = [x.replace(")", "").replace("(", "") for x in tokens_unprocessed]
    floats = [float(x) for x in tokens]
    time, ftx, fty, ftz, fpx, fpy, fpz, fvx, fvy, fvz = \
        floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], \
        floats[6], floats[7], floats[8], floats[9]

    return (time,
            ftx, fty, ftz,
            fpx, fpy, fpz,
            fvx, fvy, fvz)


def _line2values_old_format(line: str) -> Tuple[float, ...]:
    r"""Convert a line of a postProcessing/forces/<timestep>/forces.dat file to numeric values
    for an older format where forces and moments are in the same file

    Parameters
    ----------
    line : line from postProcessing/forces/<timestep>/forces.dat

    """
    tokens_unprocessed = line.split()
    tokens = [x.replace(")", "").replace("(", "") for x in tokens_unprocessed]
    floats = [float(x) for x in tokens]
    time, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, \
        mpx, mpy, mpz, mvx, mvy, mvz, mpox, mpoy, mpoz = \
        floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], \
        floats[6], floats[7], floats[8], floats[9], \
        floats[10], floats[11], floats[12], floats[13], floats[14], \
        floats[15], floats[16], floats[17], floats[18]

    return (time,
            fpx, fpy, fpz,
            fvx, fvy, fvz,
            fpox, fpoy, fpoz,
            mpx, mpy, mpz,
            mvx, mvy, mvz,
            mpox, mpoy, mpoz)


def animate(frame: int, *fargs: List[Any]) -> None:
    r"""Function for the matplotlib animation.FuncAnimation call"""
    times, ftxs, ftys, ftzs, fpxs, fpys, fpzs, fvxs, fvys, fvzs= \
        [], [], [], [], [], [], [], [], [], []

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
                    _line2values(line)
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
                _, _, _, _, _, _, _, _, _ = _line2values_old_format(line)
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
    from argparse import ArgumentParser
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
    ani = animation.FuncAnimation(fig, animate, fargs=[args.timestep, args.last, args.precision], interval=args.refresh * 1000)
    plt.show()
