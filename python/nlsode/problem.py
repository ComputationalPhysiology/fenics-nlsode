import dolfin


class NonlinearProblem(dolfin.NonlinearProblem):
    def __init__(self, J, F, bcs):
        super().__init__()
        self._J = J
        self._F = F
        if not isinstance(bcs, (list, tuple)):
            bcs = [bcs]
        self.bcs = bcs

    def F(self, b: dolfin.PETScVector, x: dolfin.PETScVector):
        dolfin.assemble(self._F, tensor=b)
        for bc in self.bcs:
            bc.apply(b, x)

    def J(self, A: dolfin.PETScMatrix, x: dolfin.PETScVector):
        dolfin.assemble(self._J, tensor=A)
        for bc in self.bcs:
            bc.apply(A)
