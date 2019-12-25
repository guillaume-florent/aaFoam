#!/usr/bin/env python
# coding: utf-8

"""Parser for OpenFOAM field data and diff-ing"""

import sys
from os.path import basename, dirname, join
import struct
from typing import Tuple, List, Dict, Union
import numpy as np

# ************ *
# Field parser *
# ************ *


def parse_field_all(fn: str) -> Tuple[List[bytes], np.ndarray, dict, int, int, int]:
    """Parse internal field, extract data to numpy.array

    Parameters
    ----------
    fn : file name

    Returns
    -------
    numpy array of internal field and boundary dict

    """
    with open(fn, "rb") as f:
        content = f.readlines()
        internal, n, n2, num = _parse_internal_field_content(content)
        boundary= _parse_boundary_content(content)
        return content, internal, boundary, n, n2, num


def parse_internal_field(fn: str) -> np.ndarray:
    """Parse internal field, extract data to numpy.array

    Parameters
    ----------
    fn : file name

    Returns
    -------
    numpy array of internal field

    """
    with open(fn, "rb") as f:
        content = f.readlines()
        return _parse_internal_field_content(content)


def _parse_internal_field_content(content: List[bytes]) -> Union[np.ndarray, Tuple[np.ndarray, int, int, int]]:
    """Parse internal field from content

    Parameters
    ----------
    content: contents of lines

    Returns
    -------
    numpy array of internal field

    """
    is_binary = _is_binary_format(content)
    for ln, lc in enumerate(content):
        if lc.startswith(b'internalField'):
            if b'nonuniform' in lc:
                return _parse_data_nonuniform(content, ln, len(content), is_binary)
            elif b'uniform' in lc:
                return _parse_data_uniform(content[ln])
            break
            # TODO : elif raise instead of break
    return None


def parse_boundary_field(fn: str) -> Dict[bytes, Dict[bytes, Union[np.ndarray, float]]]:
    """Parse boundary field, extract to dict

    Parameters
    ----------
    fn: file name

    Returns
    -------
    dict of boundary field

    """
    with open(fn, "rb") as f:
        content = f.readlines()
        return _parse_boundary_content(content)


def _parse_boundary_content(content: List[bytes]) -> Dict[bytes, Dict[bytes, Union[np.ndarray, float]]]:
    """Parse each boundary from boundaryField

    Parameters
    ----------
    content :

    Returns
    -------

    """
    data = {}
    is_binary = _is_binary_format(content)
    bd = _split_boundary_content(content)

    for boundary, (n1, n2) in bd.items():
        pd = {}
        n = n1
        while True:
            lc = content[n]
            if b'nonuniform' in lc:
                v, _, _, _ = _parse_data_nonuniform(content, n, n2, is_binary)
                pd[lc.split()[0]] = v
                if not is_binary:
                    n += len(v) + 4
                else:
                    n += 3
                continue
            elif b'uniform' in lc:
                pd[lc.split()[0]] = _parse_data_uniform(content[n])
            n += 1
            if n > n2:
                break
        data[boundary] = pd
    return data


def _parse_data_uniform(line: bytes) -> Union[np.ndarray, float]:
    """Parse uniform data from a line

    Parameters
    ----------
    line: a line include uniform data, eg. "value           uniform (0 0 0);"

    Returns
    -------
    data

    """
    if b'(' in line:
        return np.array([float(x) for x in line.split(b'(')[1].split(b')')[0].split()])
    return float(line.split(b'uniform')[1].split(b';')[0])


def _parse_data_nonuniform(content: List[bytes], n: int, n2: int, is_binary: bool) -> Tuple[np.ndarray, int, int, int]:
    """Parse nonuniform data from lines

    Parameters
    ----------
    content: data content
    n: line number
    n2: last line number
    is_binary: binary format or not

    Returns
    -------
    data

    """
    num = int(content[n + 1])
    # print(n, n2, num)
    if not is_binary:
        if b'scalar' in content[n]:
            data = np.array([float(x) for x in content[n + 3:n + 3 + num]])
        else:
            data = np.array([ln[1:-2].split() for ln in content[n + 3:n + 3 + num]], dtype=float)
    else:
        nn = 1
        if b'vector' in content[n]:
            nn = 3
        elif b'symmtensor' in content[n]:
            nn = 6
        elif b'tensor' in content[n]:
            nn = 9
        buf = b''.join(content[n+2:n2+1])
        vv = np.array(struct.unpack('{}d'.format(num*nn),
                                    buf[struct.calcsize('c'):num*nn*struct.calcsize('d')+struct.calcsize('c')]))
        if nn > 1:
            data = vv.reshape((num, nn))
        else:
            data = vv
    return data, n, n2, num


def _split_boundary_content(content: List[bytes]) -> Dict[bytes, List[int]]:
    """Split each boundary from boundaryField

    Parameters
    ----------
    content :

    Returns
    -------
    boundary and its content range

    """
    bd = {}
    n = 0
    in_boundary_field = False
    in_patch_field = False
    current_path = ''
    while True:
        lc = content[n]
        if lc.startswith(b'boundaryField'):
            in_boundary_field = True
            if content[n+1].startswith(b'{'):
                n += 2
                continue
            elif content[n+1].strip() == b'' and content[n+2].startswith(b'{'):
                n += 3
                continue
            else:
                print('no { after boundaryField')
                break
        if in_boundary_field:
            if lc.rstrip() == b'}':
                break
            if in_patch_field:
                if lc.strip() == b'}':
                    bd[current_path][1] = n-1
                    in_patch_field = False
                    current_path = ''
                n += 1
                continue
            if lc.strip() == b'':
                n += 1
                continue
            current_path = lc.strip()
            if content[n+1].strip() == b'{':
                n += 2
            elif content[n+1].strip() == b'' and content[n+2].strip() == b'{':
                n += 3
            else:
                print('no { after boundary patch')
                break
            in_patch_field = True
            bd[current_path] = [n, n]
            continue
        n += 1
        if n > len(content):
            if in_boundary_field:
                print('error, boundaryField not end with }')
            break

    return bd


def _is_binary_format(content: List[bytes], maxline: int = 20) -> bool:
    """Parse file header to judge the format is binary or not

    Parameters
    ----------
    content: file content in line list
    maxline: maximum lines to parse

    Returns
    -------
    binary format or not

    """
    for lc in content[:maxline]:
        if b'format' in lc:
            if b'binary' in lc:
                return True
            return False
    return False

# ******* *
# Diffing *
# ******* *


def diff_non_uniform_fields(file_1, file_2, percentage=False):
    r"""Substract the data in file 2 from the data in file 1, write to<file_2>_diff in the folder of file_1"""
    content, internal, boundary, n, n2, num = parse_field_all(file_1)
    content2, internal2, boundary2, n_2, n2_2, num_2 = parse_field_all(file_2)

    assert n == n_2
    assert n2 == n2_2
    assert num == num_2

    if percentage is False:
        data1_minus_data2 = internal2 - internal
    else:
        data1_minus_data2 = np.divide(internal2 - internal,
                                      internal,
                                      out=np.zeros_like(internal2 - internal),
                                      where=internal != 0) * 100
        data1_minus_data2[data1_minus_data2 == np.inf] = sys.float_info.max
        data1_minus_data2 = np.nan_to_num(data1_minus_data2)  # convert nans to 0

    with open(join(dirname(file_1), "%s_%s" % (basename(file_2), "_diff")), "w") as f:

        header = content[0: n+3]

        for i, line in enumerate(header):
            if b"object      U" in line:
                header[i] = line.replace(b"object      U;", b"object      U_diff;")
            if b"object      p" in line:
                header[i] = line.replace(b"object      p;", b"object      p_diff;")
            # TODO : other fields
            # TODO : the file name might give a big hint to what string has to be replaced

        for line in header:
            f.write(line.decode())

        for data_row in data1_minus_data2:
            if isinstance(data_row, float):
                f.write("%f\n" % float(data_row))
            elif isinstance(data_row, (list, np.ndarray)):
                f.write("(")
                for i, v in enumerate(data_row):
                    f.write(str(v))
                    if i != len(data_row) - 1:
                        f.write(" ")
                f.write(")")
                f.write("\n")
            else:
                raise RuntimeError("Something is not right ...")

        for line in content[n+3+num: -1]:
            f.write(line.decode())


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Live graphs of forces")
    parser.add_argument('file_1', help="First file for diff")
    parser.add_argument('file_2', help="First file for diff")
    parser.add_argument('-p', '--percentage',
                        default=False,
                        action='store_true',
                        help="Express the difference in percentage")
    args = parser.parse_args()
    # print("Percentage is %r " % args.percentage)
    f1 = args.file_1
    f2 = args.file_2
    diff_non_uniform_fields(f1, f2, percentage=args.percentage)
