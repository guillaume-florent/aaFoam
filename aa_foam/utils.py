# coding: utf-8

r"""Utility functions."""

from typing import List


def is_binary_format(content: List[bytes], maxline: int = 20) -> bool:
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
