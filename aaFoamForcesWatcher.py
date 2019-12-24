#!/usr/bin/env python
# coding: utf-8

r"""Live matplotlib plot of forces"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) \
    = plt.subplots(3, 3, sharex='col')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]


def _line2values(line):
    r"""Convert a line of a postProcessing/forces.dat file to numeric values

    Parameters
    ----------
    line : str
        reference_area line from postProcessing/forces.dat

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


def animate(i, *fargs):
    r"""Function for the matplotlib animation.FuncAnimation call"""
    times, ftxs, ftys, ftzs, fpxs, fpys, fpzs, fvxs, fvys, fvzs= \
        [], [], [], [], [], [], [], [], [], []

    timestep = fargs[0]

    with open("postProcessing/forces/%s/force.dat" % timestep) as fd:
        for line in fd:
            if line[0] == "#":
                continue
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
    titles = ['ftxs', 'ftys', 'ftzs', 'fpxs', 'fpys', 'fpzs', 'fvxs', 'fvys', 'fvzs']

    colors = {'x': "red", 'y': "green", 'z': "blue"}

    for ax, y, title in zip(axs, ys, titles):

        ax.clear()
        ax.set_title("%s (%.4f)" %(title, sum(y[-plot_last:-1]) / len(y[-plot_last:-1])))
        ax.set_ylim(min(y[-plot_last:-1])-0.0001, max(y[-plot_last:-1])+0.0001)
        ax.plot(times, y, color=colors[title[2]])
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
    args = parser.parse_args()
    plot_last = args.last
    timestep = args.timestep
    interval = args.refresh * 1000
    ani = animation.FuncAnimation(fig, animate, fargs=[timestep], interval=interval)
    plt.show()
