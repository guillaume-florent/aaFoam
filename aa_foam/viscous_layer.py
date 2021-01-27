# coding: utf-8

r"""Viscous layers computations"""

from typing import Tuple, List


def viscous_layer_mesh(thickness_first_layer: float,
                       growth_ratio: float,
                       nb_layers: int) -> Tuple[float, float, List[float]]:
    r"""Viscous layer mesh

    Parameters
    ----------
    thickness_first_layer : thickness of layer clsest to the wall
    growth_ratio : the thickness ratio between a cell and the one just inside it
    nb_layers : total number of viscous layers

    Returns
    -------
    A tuple of total thickness, thickness of outermost cell, list of thicknesses

    """
    thicknesses = [thickness_first_layer * growth_ratio ** i for i in range(nb_layers)]
    thickness_total = sum(thicknesses)  # total thickness of BL meshing
    thickness_outermost_cell = thicknesses[-1]  # outermost BL meshing cell thickness
    return thickness_total, thickness_outermost_cell, thicknesses
