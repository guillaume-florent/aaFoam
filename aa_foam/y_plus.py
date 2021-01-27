# coding: utf-8

r"""Y+ computations."""

from typing import Tuple


def y_plus_calc(u_freestream: float,
                density: float,
                mu: float,
                length: float,
                y_plus: float) -> Tuple[float, float, float]:
    r"""Y+

    Parameters
    ----------
    u_freestream : Freestream velocity [m/s]
    density : Density [kg/m3]
    mu : Dynamic viscosity [kg/m s]
    length : Reference length [m]
    y_plus : Desired y+

    Returns
    -------
    A tuple of wall spacing [m], reynolds[-], kinematic viscosity [m**2/s]

    """
    kin = mu / density
    re = u_freestream * length / kin
    cf = 0.026 / re**(1/7)
    tau_wall = cf * density * u_freestream**2 / 2
    u_fric = (tau_wall / density)**0.5
    delta_s = y_plus * mu / (u_fric * density)
    return delta_s, re, kin
