#!/usr/bin/env python
# coding: utf-8

"""Setup for aaFoam"""

import aa_foam
from distutils.core import setup

setup(name=aa_foam.__name__,
      version=aa_foam.__version__,
      description=aa_foam.__description__,
      long_description='OpenFOAM utilities',
      url=aa_foam.__url__,
      download_url=aa_foam.__download_url__,
      author=aa_foam.__author__,
      author_email=aa_foam.__author_email__,
      license=aa_foam.__license__,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
      keywords='OpenFOAM utilities',
      packages=['aa_foam'],
      package_data={},
      scripts=['bin/aaFoamCoefsWatcher.py',
               'bin/aaFoamDiff.py',
               'bin/aaFoamForcesWatcher.py',
               'bin/aaFoamVL.py',
               'bin/aaFoamYPlus.py',
               'bin/aaFoamPlotMotionLive.sh']
      )
