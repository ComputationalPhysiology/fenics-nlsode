# fenics-nlsode

WARNING: THIS REPO IS WORK IN PROGRESS AND IS NOT YET WORKING AS EXPECTED

`fenics-nlsode` is a FEniCS based nonlinear solver coupled to an ODE solver. In some cases you have a PDE with a tight coupling to an ODE meaning that the PDE solution depends on the ODE solution and vica versa. In this case you might need to re-integrate the ODE after each newton iteration in the nonlinear solver. 

This library is a re-implementation of the original [`NewtonSolver` in FEniCS](https://bitbucket.org/fenics-project/dolfin/src/master/dolfin/nls/NewtonSolver.cpp) with the additional ODE integration step after each newton iteration. 
The ODEs are solved using [`goss`](https://github.com/ComputationalPhysiology/goss)


