#!/usr/bin/env python
# coding: utf-8

r"""Viscous layers meshing computations"""

import sys
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
        # If the conversion to float or int fails, it is better when it fails here rather
        # than after printing **** INPUT ****
        first_layer_thickness = float(args.first_layer)
        growth_ratio = float(args.growth_ratio)
        nb_layers = int(args.nb_layers)

        print("**** INPUT ****")

        print(f"First layer thickness : {first_layer_thickness:.8f}")
        print(f"         Growth ratio : {growth_ratio:.3f}")
        print(f"            Nb layers : {nb_layers}")

        total, outermost, _ = viscous_layer_mesh(first_layer_thickness,
                                                 growth_ratio,
                                                 nb_layers)

        print("**** OUTPUT ****")

        print(f"         Total thickness : {total:.8f}")
        print(f"Outermost cell thickness : {outermost:.8f}")
    except ValueError as e:
        print(f"ERROR : {e}")
        sys.exit(1)
