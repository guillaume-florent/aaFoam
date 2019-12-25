aaFoamDiff.py
-------------

******** Percentage option
******** Add logging
******** Checks (file names, number of values ...)
******** Handle errors
******** U -> U_diff, p -> p_diff    for other fields too!

aaForcesWatcher*.py
-------------------

******** Unify both files
******** Typing
******** Pretify plots and titles ...
******** Add a precision option for the number of significant digits in averages above plots
Live change of params (tkinter UI? interprocess com?)
If building a more elaborate UI, use tkinter (included with Python, no cumbersome PyQt of Wx installs)

Tests
-----

Add them !


real pressure in incompressible flow  (aaFoamMult)
------------------------------------
p file -> p_real file


New
---

Memory usage of a case -> see _Repositories/wip/ps_mem
-> aaFoamVL -> VL = Viscous layers -> outer cell thickness and total thickness
                                     from first layer thickness, progression and expansion ratio
-> aaFoamBL -> theoretical BL thickness
aaFoamYPlus -> Y+ calculator (same as Pointwise online calc)
aaFoamGrading -> grading calculations for blockMesh (same as online)
aaFoamFrictionLines -> theoretical friction line computations to check against CFD results
