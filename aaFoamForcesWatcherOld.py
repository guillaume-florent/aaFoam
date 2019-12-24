#!/usr/bin/env python
# coding: utf-8

r"""Live matplotlib plot of forces for an older format where forces and moments are in the same file"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation

plot_last = 100

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) \
    = plt.subplots(3, 3, sharex='col')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]


def _line2values(line):
    r"""Convert a line of a postProcessing/forces.dat file to numeric values

    Parameters
    ----------
    line : str
        reference_area line from postProcessing/forces.dat"""
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


def animate(i):
    r"""Function for the matplotlib animation.FuncAnimation call"""
    times, fpxs, fpys, fpzs, fvxs, fvys, fvzs, fpoxs, fpoys, fpozs = \
        [], [], [], [], [], [], [], [], [], []
    with open("postProcessing/forces/0/forces.dat") as fd:
        for line in fd:
            if line[0] == "#":
                continue
            # time, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, \
            #     mpx, mpy, mpz, mvx, mvy, mvz, mpox, mpoy, mpoz = \
            time, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, \
            _, _, _, _, _, _, _, _, _ = _line2values(line)
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
    titles = ['fpxs', 'fpys', 'fpzs', 'fvxs', 'fvys', 'fvzs',
              'fpoxs', 'fpoys', 'fpozs']

    for ax, y, title in zip(axs, ys, titles):

        ax.clear()
        ax.set_title(title)
        ax.set_ylim(min(y[-plot_last:-1]), max(y[-plot_last:-1]))
        ax.plot(times, y)


if __name__ == "__main__":
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
