import mpi4py

from . import _nlsodecpp


class NewtonSolver(_nlsodecpp.NewtonSolver):
    def __init__(self, comm: mpi4py.MPI.Comm):

        super().__init__()
        # FIXME: Need to figure out how to do the bindings for
        # the MPI communicator
        # super().__init__(
        #     comm,
        #     dolfin.PETScKrylovSolver(),
        #     dolfin.PETScFactory.instance(),
        # )
