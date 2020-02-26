aaForcesWatcher*.py / aaFoamCoefsWatcher.py
-------------------------------------------

Live change of params (tkinter UI? interprocess com?)
If building a more elaborate UI, use tkinter (included with Python, no cumbersome PyQt of Wx installs)

Tests
-----

Add them !

New
---

********* aaFoamVL -> VL = Viscous layers -> outer cell thickness and total thickness from first layer thickness, progression and expansion ratio
******** aaFoamYPlus -> Y+ calculator (same as Pointwise online calc)
Memory usage of a case -> see _Repositories/wip/ps_mem
aaFoamGrading -> grading calculations for blockMesh (same as online)
aaFoamFrictionLines -> theoretical friction line computations to check against CFD results
-> aaFoamBL -> theoretical BL thickness
real pressure in incompressible flow  (aaFoamMult) : p file -> p_real file
