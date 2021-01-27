#!/usr/bin/env python
# coding: utf-8

r"""Number of cells and expansion ratio from L, xmin, xmax"""

import sys
import logging
from argparse import ArgumentParser
from aa_foam.grading import number_of_cells_and_expansion_ratio

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="Number of cells and expansion ratio from L, xmin, xmax")
    parser.add_argument('L', help="Length [m]")
    parser.add_argument('x_min', help="Minimum / starting cell size [m]")
    parser.add_argument('x_max', help="Maximum / ending cell size [m]")

    args = parser.parse_args()

    try:
        # If the conversion to float or int fails, it is better when it fails here rather
        # than after printing **** INPUT ****
        L = float(args.L)
        x_min = float(args.x_min)
        x_max = float(args.x_max)

        logger.info("**** INPUT ****")

        logger.info(f"    L [m] : {L:.8f}")
        logger.info(f"x_min [m] : {x_min:.8f}")
        logger.info(f"x_max [m] : {x_max:.8f}")

        N, R, r = number_of_cells_and_expansion_ratio(L, x_min, x_max)

        logger.info("**** OUTPUT ****")

        logger.info(f"       Number of cells : {N}")
        logger.info(f"Size ratio (max / min) : {R:.8f}")
        logger.info(f"          Growth ratio : {r:.8f}")
    except ValueError as e:
        # logger.error(e)
        print(f"ERROR : {e}")
        sys.exit(1)
