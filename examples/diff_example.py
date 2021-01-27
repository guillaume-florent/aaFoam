#!/usr/bin/env python
# coding: utf-8

r"""Example of diff-ing 2 OpenFOAM non uniform field files"""

import logging

from aa_foam.diffing import diff_non_uniform_fields

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: %(message)s')

    # Compute the percentage difference of U. Write the results to ../sample_data/2/U__diff
    diff_non_uniform_fields(file_1="../sample_data/2/U",
                            file_2="../sample_data/1/U",
                            percentage=True)

    # Compute the absolute difference of p. Write the results to ../sample_data/2/p__diff
    diff_non_uniform_fields(file_1="../sample_data/2/p",
                            file_2="../sample_data/1/p",
                            percentage=False)
