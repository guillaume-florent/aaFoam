# coding: utf-8

r"""OpenFOAM computed forces handling"""

from typing import Tuple


def force_line2values(line: str) -> Tuple[float, ...]:
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


def force_line2values_old_format(line: str) -> Tuple[float, ...]:
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
