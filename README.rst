.. -*- coding: utf-8 -*-

******
aaFoam
******

OpenFOAM utilities, work in progress ...

Utilities
---------

Field files diffing
~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

  aaFoamDiff.py file_1 file_2

Works on **non uniform** field files (timestep > 0     /U /p ....) that are defined on **identical meshes**.

Produces a *<field>_diff* file in the folder of *file_1*

The values are file_1 minus file_2


Forces monitoring
~~~~~~~~~~~~~~~~~

.. code-block:: shell

  aaFoamForcesWatcher.py -l 50

  aaFoamForcesWatcher.py -h

Run at case root, during the run or when the case is solved

Opens a live plot of the forces (requires the forces function in system/controlDict) as it reads the *postProcessing/forces/0/force.dat* file.


Requirements
------------

Python 3, numpy & matplotlib


Thanks
------

Most of the OpenFOAM files parsing code come from https://github.com/dayigu

