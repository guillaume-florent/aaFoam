#!/usr/bin/env python
# coding: utf-8

r"""Example of diff-ing 2 OpenFOAM non uniform field files"""

from aaFoamDiff import diff_non_uniform_fields


if __name__ == "__main__":
    diff_non_uniform_fields("../data/2/U", "../data/1/U", percentage=True)
    diff_non_uniform_fields("../data/2/p", "../data/1/p", percentage=False)
