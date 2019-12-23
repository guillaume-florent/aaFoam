# coding: utf-8

"""Mesh parser (OpenFOAM polymesh) from https://github.com/dayigu"""

import os
from collections import namedtuple
import struct
from typing import Tuple, List, Dict, Union, Generator, Callable
import numpy as np

from aaFoamDiff import parse_internal_field, _is_binary_format

Boundary = namedtuple('Boundary', 'type, num, start, id')


def _is_integer(s):
    try:
        _ = int(s)
        return True
    except ValueError:
        return False


class FoamMesh(object):
    """ FoamMesh class """
    def __init__(self, path: str):
        self.path = os.path.join(path, "constant/polyMesh/")
        self._parse_mesh_data(self.path)
        self.num_point = len(self.points)
        self.num_face = len(self.owner)
        self.num_inner_face = len(self.neighbour)
        self.num_cell = max(self.owner)
        self._set_boundary_faces()
        self._construct_cells()
        self.cell_centres = None
        self.cell_volumes = None
        self.face_areas = None

    def read_cell_centres(self, fn: str):
        """Read cell centres coordinates from data file,
        the file can be got by `postProcess -func 'writeCellCentres' -time 0'

        Parameters
        ----------
        fn: cell centres file name, eg. '0/C'

        """
        self.cell_centres = parse_internal_field(fn)

    def read_cell_volumes(self, fn: str):
        """Read cell volumes from data file,
        the file can be got by `postProcess -func 'writeCellVolumes' -time 0'

        Parameters
        ----------
        fn: cell centres file name, eg. '0/C'

        """
        self.cell_volumes = parse_internal_field(fn)

    def read_face_areas(self, fn: str):
        """Read face areas from data file,

        Parameters
        ----------
        fn: cell centres file name, eg. '0/C'

        """
        self.face_areas = parse_internal_field(fn)

    def cell_neighbour_cells(self, i: int) -> List[int]:
        """Return neighbour cells of cell i

        Parameters
        ----------
        i: cell index

        Returns
        -------
        neighbour cell list

        """
        return self.cell_neighbour[i]

    def is_cell_on_boundary(self, i: int, bd: str = None) -> bool:
        """Check if cell i is on boundary bd

        Parameters
        ----------
        i: cell index, 0<=i<num_cell
        bd: boundary name, byte str

        """
        if i < 0 or i >= self.num_cell:
            return False
        if bd is not None:
            try:
                bid = self.boundary[bd].id
            except KeyError:
                return False
        for n in self.cell_neighbour[i]:
            if bd is None and n < 0:
                return True
            elif bd and n == bid:
                return True
        return False

    def is_face_on_boundary(self, i: int, bd: str = None) -> bool:
        """Check if face i is on boundary bd

        Parameters
        ----------
        i: face index, 0<=i<num_face
        bd: boundary name, byte str

        """
        if i < 0 or i >= self.num_face:
            return False
        if bd is None:
            if self.neighbour[i] < 0:
                return True
            return False
        try:
            bid = self.boundary[bd].id
        except KeyError:
            return False
        if self.neighbour[i] == bid:
            return True
        return False

    def boundary_cells(self, bd: str) -> Union[Tuple, Generator]:
        """Return cell id list on boundary bd

        Parameters
        ----------
        bd: boundary name, byte str

        Returns
        -------
        cell id generator

        """
        try:
            b = self.boundary[bd]
            return (self.owner[f] for f in range(b.start, b.start+b.num))
        except KeyError:
            return ()

    def _set_boundary_faces(self) -> None:
        """Set faces' boundary id which on boundary"""
        self.neighbour.extend([-10]*(self.num_face - self.num_inner_face))
        for b in self.boundary.values():
            self.neighbour[b.start:b.start+b.num] = [b.id]*b.num

    def _construct_cells(self) -> None:
        """Construct cell faces, cell neighbours"""
        cell_num = max(self.owner) + 1
        self.cell_faces = [[] for _ in range(cell_num)]
        self.cell_neighbour = [[] for _ in range(cell_num)]
        for i, n in enumerate(self.owner):
            self.cell_faces[n].append(i)
        for i, n in enumerate(self.neighbour):
            if n >= 0:
                self.cell_faces[n].append(i)
                self.cell_neighbour[n].append(self.owner[i])
            self.cell_neighbour[self.owner[i]].append(n)

    def _parse_mesh_data(self, path) -> None:
        """Parse mesh data from mesh files

        Parameters
        ----------
        path: path of mesh files

        """
        self.boundary = self.parse_mesh_file(os.path.join(path, 'boundary'), self.parse_boundary_content)
        self.points = self.parse_mesh_file(os.path.join(path, 'points'), self.parse_points_content)
        self.faces = self.parse_mesh_file(os.path.join(path, 'faces'), self.parse_faces_content)
        self.owner = self.parse_mesh_file(os.path.join(path, 'owner'), self.parse_owner_neighbour_content)
        self.neighbour = self.parse_mesh_file(os.path.join(path, 'neighbour'), self.parse_owner_neighbour_content)

    @classmethod
    def parse_mesh_file(cls, fn: str, parser: Callable) -> Union[np.ndarray, List, Dict]:
        """Parse mesh file

        Parameters
        ----------
        fn: boundary file name
        parser: parser of the mesh

        Returns
        -------
        mesh data

        """
        try:
            with open(fn, "rb") as f:
                content = f.readlines()
                return parser(content, _is_binary_format(content))
        except FileNotFoundError:
            print('file not found: %s' % fn)
            return None

    @classmethod
    def parse_points_content(cls, content: List[bytes], is_binary: bool, skip: int = 10) -> np.ndarray:
        """Parse points from content

        Parameters
        ----------
        content: file contents
        is_binary: binary format or not
        skip: skip lines

        Returns
        -------
        points coordinates as numpy.array

        """
        n = skip
        while n < len(content):
            lc = content[n]
            if _is_integer(lc):
                num = int(lc)
                if not is_binary:
                    data = np.array([ln[1:-2].split() for ln in content[n + 2:n + 2 + num]], dtype=float)
                else:
                    buf = b''.join(content[n+1:])
                    disp = struct.calcsize('c')
                    vv = np.array(struct.unpack('{}d'.format(num*3),
                                                buf[disp:num*3*struct.calcsize('d') + disp]))
                    data = vv.reshape((num, 3))
                return data
            n += 1
        return None

    @classmethod
    def parse_owner_neighbour_content(cls, content: List[bytes], is_binary: bool, skip: int = 10) -> List[int]:
        """Parse owner or neighbour from content

        Parameters
        ----------
        content: file contents
        is_binary: binary format or not
        skip: skip lines

        Returns
        -------
        indexes as list

        """
        n = skip
        while n < len(content):
            lc = content[n]
            if _is_integer(lc):
                num = int(lc)
                if not is_binary:
                    data = [int(ln) for ln in content[n + 2:n + 2 + num]]
                else:
                    buf = b''.join(content[n+1:])
                    disp = struct.calcsize('c')
                    data = struct.unpack('{}i'.format(num),
                                         buf[disp:num*struct.calcsize('i') + disp])
                return list(data)
            n += 1
        return None

    @classmethod
    def parse_faces_content(cls, content: List[bytes], is_binary: bool, skip: int = 10) -> List[int]:
        """Parse faces from content

        Parameters
        ----------
        content: file contents
        is_binary: binary format or not
        skip: skip lines

        Returns
        -------
        faces as list

        """
        n = skip
        while n < len(content):
            lc = content[n]
            if _is_integer(lc):
                num = int(lc)
                if not is_binary:
                    data = [[int(s) for s in ln[2:-2].split()] for ln in content[n + 2:n + 2 + num]]
                else:
                    buf = b''.join(content[n+1:])
                    disp = struct.calcsize('c')
                    idx = struct.unpack('{}i'.format(num), buf[disp:num*struct.calcsize('i') + disp])
                    disp = 3*struct.calcsize('c') + 2*struct.calcsize('i')
                    pp = struct.unpack('{}i'.format(idx[-1]),
                                       buf[disp+num*struct.calcsize('i'):
                                           disp+(num+idx[-1])*struct.calcsize('i')])
                    data = []
                    for i in range(num - 1):
                        data.append(pp[idx[i]:idx[i+1]])
                return data
            n += 1
        return None

    @classmethod
    def parse_boundary_content(cls, content: List[bytes], is_binary: bool = None, skip: int = 10) -> dict:
        """Parse boundary from content

        Parameters
        ----------
        content: file contents
        is_binary: binary format or not, not used
        skip: skip lines

        Returns
        -------
        boundary dict

        """
        bd = {}
        num_boundary = 0
        n = skip
        bid = 0
        in_boundary_field = False
        in_patch_field = False
        current_patch = b''
        current_type = b''
        current_nFaces = 0
        current_start = 0
        while True:
            if n > len(content):
                if in_boundary_field:
                    print('error, boundaryField not end with )')
                break
            lc = content[n]
            if not in_boundary_field:
                if _is_integer(lc.strip()):
                    num_boundary = int(lc.strip())
                    in_boundary_field = True
                    if content[n + 1].startswith(b'('):
                        n += 2
                        continue
                    elif content[n + 1].strip() == b'' and content[n + 2].startswith(b'('):
                        n += 3
                        continue
                    else:
                        print('no ( after boundary number')
                        break
            if in_boundary_field:
                if lc.startswith(b')'):
                    break
                if in_patch_field:
                    if lc.strip() == b'}':
                        in_patch_field = False
                        bd[current_patch] = Boundary(current_type, current_nFaces, current_start, -10-bid)
                        bid += 1
                        current_patch = b''
                    elif b'nFaces' in lc:
                        current_nFaces = int(lc.split()[1][:-1])
                    elif b'startFace' in lc:
                        current_start = int(lc.split()[1][:-1])
                    elif b'type' in lc:
                        current_type = lc.split()[1][:-1]
                else:
                    if lc.strip() == b'':
                        n += 1
                        continue
                    current_patch = lc.strip()
                    if content[n + 1].strip() == b'{':
                        n += 2
                    elif content[n + 1].strip() == b'' and content[n + 2].strip() == b'{':
                        n += 3
                    else:
                        print('no { after boundary patch')
                        break
                    in_patch_field = True
                    continue
            n += 1

        return bd
