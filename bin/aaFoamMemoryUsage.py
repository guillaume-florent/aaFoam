#!/usr/bin/env python
# coding: utf-8

r"""Memory usage

Run:
> aaFoamMemoryUsage.py -p <PID>

Do not use sudo, the command won't be found.

"""

from aa_foam.memory_usage import memory_usage_main

if __name__ == '__main__':
    memory_usage_main()
