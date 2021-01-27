# coding: utf-8

r"""OpenFOAM computed force coefficients handling"""

from typing import Tuple


def coefficients_line2values(line: str) -> Tuple[float, ...]:
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
