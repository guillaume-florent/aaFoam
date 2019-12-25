#!/usr/bin/env python
# coding: utf-8

r"""Example of diff-ing 2 OpenFOAM non uniform field files"""

import logging

from aaFoamDiff import diff_non_uniform_fields

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: %(message)s')
    diff_non_uniform_fields("../data/2/U", "../data/1/U", percentage=True)
    diff_non_uniform_fields("../data/2/p", "../data/1/p", percentage=False)
