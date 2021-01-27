# coding: utf-8

r"""Grading computations

Grading computations from :
https://github.com/aqeelahmed168/OpenFoamCaseSetupWithPython

"""

from typing import Tuple
import logging

import numpy as np
from scipy.optimize import fsolve

logger = logging.getLogger(__name__)


def number_of_cells_and_expansion_ratio(L: float,
                                        xmin: float,
                                        xmax: float) -> Tuple[int, float, float]:
    """ Get number of cells and expansion ratio given the Length of domain,
    min and max cell size.

    Parameters
    ----------
    L : length of domain
    xmin : minimum cell size
    xmax : maximum cell size

    Returns
    -------
    N : number of cells
    R : size ratio (max cell size / min cell size) aka grading
    r: local growth ratio (size ratio between adjacent cells)

    """
    if L <= 0:
        msg = "L should be strictly positive"
        logger.error(msg)
        raise ValueError(msg)
    if xmin <= 0:
        msg = "xmin should be strictly positive"
        logger.error(msg)
        raise ValueError(msg)
    if xmax <= 0:
        msg = "xmax should be strictly positive"
        logger.error(msg)
        raise ValueError(msg)
    if xmax < xmin:
        msg = "xmax should be greater than or equal to xmin"
        logger.error(msg)
        raise ValueError(msg)
    if xmax > L / 2:
        msg = "xmax should be smaller than half the domain length"
        logger.error(msg)
        raise ValueError(msg)

    #   FirstToLastCellExpansionRatio
    R = xmax / xmin

    #   CellToCellExpansionRatio
    r = (L - xmin) / (L - (xmin * R))

    #   Number of cells
    if xmin == xmax:
        N = np.ceil(L / xmin)
    else:
        N = np.ceil(np.log(R) / np.log(r) + 1)

    return int(N), R, r


def expansion_ratio_from_cells_and_length(L: float,
                                          xmin: float,
                                          N: int) -> Tuple[float, float]:
    """ Get expansion ratio given the Length of domain, number of cells,
    and min cell size.

    Parameters
    ----------
    L: length of domain
    xmin : minimum cell size
    N : number of cells

    Returns
    -------
    R : size ratio (max cell size / min cell size) aka grading
    r : local growth ratio (size ratio between adjacent cells)

    """
    if L <= 0:
        msg = "L should be strictly positive"
        logger.error(msg)
        raise ValueError(msg)
    if xmin <= 0:
        msg = "xmin should be strictly positive"
        logger.error(msg)
        raise ValueError(msg)
    if N <= 0 or not isinstance(N, int):
        msg = "The number of cells should be an int >= 1"
        logger.error(msg)
        raise ValueError(msg)
    if xmin > L / 2:
        msg = "xmin should be smaller than half the domain length"
        logger.error(msg)
        raise ValueError(msg)

    def func(R):
        return np.log(R) / np.log((L - xmin) / (L - (xmin * R))) + 1 - N

    R = fsolve(func, 1.01)
    r = R ** (1 / (N - 1))
    return R, r
