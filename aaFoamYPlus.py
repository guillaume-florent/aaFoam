#!/usr/bin/env python
# coding: utf-8

r"""yPlus computations

example use:
aaFoamYPlus.py 1 1.225 0.000018375 1 1

"""

import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)


def y_plus_calc(u_freestream: float,
                density: float,
                mu: float,
                length: float,
                y_plus: float) -> Tuple[float, float, float]:
    r"""Y+

    Parameters
    ----------
    u_freestream
    density
    mu
    length
    y_plus

    Returns
    -------
    A tuple of wall spacing, reynolds, kinematic viscosity

    """
    kin = mu / density
    re = u_freestream * length / kin
    cf = 0.026 / re**(1/7)
    tau_wall = cf * density * u_freestream**2 / 2
    u_fric = (tau_wall / density)**0.5
    delta_s = y_plus * mu / (u_fric * density)
    return delta_s, re, kin


if __name__ == "__main__":
    from argparse import ArgumentParser

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="YPlus computations")
    parser.add_argument('u_inf', help="Freestream velocity [m/s}")
    parser.add_argument('rho', help="Freestream density [kg/m3]")
    parser.add_argument('mu', help="Dynamic viscosity [kg/m s]")
    parser.add_argument('L', help="Reference length [m]")
    parser.add_argument('y_plus', help="Desired y+")

    args = parser.parse_args()

    try:
        logger.info("**** INPUT ****")

        logger.info("    U [m/s] : %.8f" % float(args.u_inf))
        logger.info("rho [kg/m3] : %.3f" % float(args.rho))
        logger.info("mu [kg/m.s] : %.8f" % float(args.mu))
        logger.info("      L [m] : %.6f" % float(args.L))
        logger.info("         y+ : %.3f" % float(args.y_plus))

        delta_s, re_x, nu = y_plus_calc(float(args.u_inf),
                                        float(args.rho),
                                        float(args.mu),
                                        float(args.L),
                                        float(args.y_plus))

        logger.info("**** OUTPUT ****")

        logger.info("Delta S (wall spacing) : %.8f" % delta_s)
        logger.info("       Reynolds number : %.8f" % re_x)
        logger.info("   Kinematic viscosity : %.8f" % nu)
    except ValueError as e:
        logger.error(e)
