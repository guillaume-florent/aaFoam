#!/usr/bin/env python
# coding: utf-8

"""Parser for OpenFOAM field data and diff-ing"""

import logging
from argparse import ArgumentParser
from aa_foam.diffing import diff_non_uniform_fields

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s :: %(levelname)6s :: %(message)s')

    parser = ArgumentParser(description="Diff-ing (of data, meaning data1 minus data2) of 2 OpenFOAM files")
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
    pct_opt = args.percentage

    try:
        diff_non_uniform_fields(f1, f2, percentage=pct_opt)
    except AssertionError as e:
        logger.error(e)
        print(e)
    except FileNotFoundError as e:
        logger.error(e)
        print(e)
