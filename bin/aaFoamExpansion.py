#!/usr/bin/env python
# coding: utf-8

r"""Expansion ratio from nb cells, starting length and domain length"""

import sys
import logging
from argparse import ArgumentParser
from aa_foam.grading import expansion_ratio_from_cells_and_length

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="Expansion ratio from nb cells, starting length and domain length")
    parser.add_argument('L', help="Length [m]")
    parser.add_argument('x_min', help="Minimum / starting cell size [m]")
    parser.add_argument('N', help="Nb cells")

    args = parser.parse_args()

    try:
        # If the conversion to float or int fails, it is better when it fails here rather
        # than after printing **** INPUT ****
        L = float(args.L)
        x_min = float(args.x_min)
        N = int(args.N)

        logger.info("**** INPUT ****")

        logger.info(f"    L [m] : {L:.8f}")
        logger.info(f"x_min [m] : {x_min:.8f}")
        logger.info(f" Nb cells : {N}")

        R, r = expansion_ratio_from_cells_and_length(L, x_min, N)

        logger.info("**** OUTPUT ****")

        logger.info(f"Size ratio (max / min) : {float(R):.8f}")
        logger.info(f"          Growth ratio : {float(r):.8f}")
    except ValueError as e:
        # logger.error(e)
        print(f"ERROR : {e}")
        sys.exit(1)
