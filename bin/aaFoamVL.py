#!/usr/bin/env python
# coding: utf-8

r"""Viscous layers meshing computations"""

import logging
from argparse import ArgumentParser
from aa_foam.viscous_layer import viscous_layer_mesh

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="Viscous layers meshing computations")
    parser.add_argument('first_layer', help="First layer thickness")
    parser.add_argument('growth_ratio', help="Expansion ratio")
    parser.add_argument('nb_layers', help="Number of layers")

    args = parser.parse_args()

    try:
        logger.info("**** INPUT ****")

        logger.info("First layer thickness : %.8f" % float(args.first_layer))
        logger.info("         Growth ratio : %.3f" % float(args.growth_ratio))
        logger.info("            Nb layers : %i" % int(args.nb_layers))

        total, outermost, _ = viscous_layer_mesh(float(args.first_layer), float(args.growth_ratio), int(args.nb_layers))

        logger.info("**** OUTPUT ****")

        logger.info("         Total thickness : %.8f" % total)
        logger.info("Outermost cell thickness : %.8f" % outermost)
    except ValueError as e:
        logger.error(e)
