#!/usr/bin/env python
# coding: utf-8

r"""Viscous layers meshing computations"""

import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)


def viscous_layer_mesh(thickness_first_layer: float, growth_ratio: float, nb_layers: int) -> Tuple[float, float, List[float]]:
    r"""Viscous layer mesh

    Parameters
    ----------
    thickness_first_layer : thickness of layer clsest to the wall
    growth_ratio : the thickness ratio between a cell and the one just inside it
    nb_layers = total number of viscous layers

    Returns
    -------
    A tuple of total thickness, thickness of outermost cell, list of thicknesses

    """
    thicknesses = [thickness_first_layer * growth_ratio ** i for i in range(nb_layers)]
    thickness_total = sum(thicknesses)  # total thickness of BL meshing
    thickness_outermost_cell = thicknesses[-1]  # outermost BL meshing cell thickness
    return thickness_total, thickness_outermost_cell, thicknesses


if __name__ == "__main__":
    from argparse import ArgumentParser

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
