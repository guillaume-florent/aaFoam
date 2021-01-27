# coding: utf-8

r"""OpenFOAM VOF utilities

See Also
--------
https://github.com/dayigu

"""

from typing import Union
import numpy as np

from aa_foam.mesh_parser import FoamMesh


def calc_phase_surface_area(mesh: FoamMesh,
                            phi: np.ndarray,
                            face_area: Union[float, list, np.ndarray] = None,
                            omg: float = 1.5) -> float:
    """Calculate phase surface area for VOF

    Parameters
    ----------
    mesh: FoamMesh object
    phi: vof data, numpy array
    face_area: face area, scalar or list or numpy array
    omg: power index

    Returns
    -------
    phase surface area

    """
    if face_area is not None:
        try:
            if len(face_area) == 1:
                face_area = [face_area[0]] * mesh.num_face
        except TypeError:
            face_area = [face_area] * mesh.num_face
    else:
        if mesh.face_areas is None:
            face_area = [1.] * mesh.num_face
        else:
            face_area = mesh.face_areas
    return sum([face_area[n]*abs(phi[mesh.owner[n]] - phi[mesh.neighbour[n]])**omg for n in range(mesh.num_inner_face)])
