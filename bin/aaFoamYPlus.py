#!/usr/bin/env python
# coding: utf-8

r"""yPlus computations

example use:
aaFoamYPlus.py 1 1.225 0.000018375 1 1

"""

import sys
import logging
from argparse import ArgumentParser
from aa_foam.y_plus import y_plus_calc

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="YPlus computations")
    parser.add_argument('u_inf', help="Freestream velocity [m/s]")
    parser.add_argument('rho', help="Density [kg/m3]")
    parser.add_argument('mu', help="Dynamic viscosity [kg/m s]")
    parser.add_argument('L', help="Reference length [m]")
    parser.add_argument('y_plus', help="Desired y+")

    args = parser.parse_args()

    try:
        # If the conversion to float or int fails, it is better when it fails here rather
        # than after printing **** INPUT ****
        u_inf = float(args.u_inf)
        rho = float(args.rho)
        mu = float(args.mu)
        L = float(args.L)
        y_plus = float(args.y_plus)

        logger.info("**** INPUT ****")

        logger.info(f"    U [m/s] : {u_inf:.8f}")
        logger.info(f"rho [kg/m3] : {rho:.3f}")
        logger.info(f"mu [kg/m.s] : {mu:.8f}")
        logger.info(f"      L [m] : {L:.6f}")
        logger.info(f"         y+ : {y_plus:.3f}")

        delta_s, re_x, nu = y_plus_calc(float(args.u_inf),
                                        float(args.rho),
                                        float(args.mu),
                                        float(args.L),
                                        float(args.y_plus))

        logger.info("**** OUTPUT ****")

        logger.info(f"Delta S (wall spacing) : {delta_s:.8f}")
        logger.info(f"       Reynolds number : {re_x:.8f}")
        logger.info(f"   Kinematic viscosity : {nu:.8f}")
    except ValueError as e:
        # logger.error(e)
        print(f"ERROR : {e}")
        sys.exit(1)
