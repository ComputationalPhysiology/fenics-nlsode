import dolfin

# import goss
from nlsode import NonlinearProblem, NewtonSolver


N = 5
mesh = dolfin.UnitCubeMesh(N, N, N)


V = dolfin.VectorFunctionSpace(mesh, "P", 1)
u = dolfin.Function(V)
v = dolfin.TestFunction(V)

F = dolfin.variable(dolfin.grad(u) + dolfin.Identity(3))
gradu = F - dolfin.Identity(3)
J = dolfin.det(F)

Ta = 60.0
f0 = dolfin.as_vector([1, 0, 0])
f = F * f0
I4f = dolfin.inner(f, f)
psi_active = dolfin.Constant(0.5) * Ta * (I4f - 1)

lmbda = 1.0
mu = 100.0
epsilon = 0.5 * (gradu + gradu.T)
psi_passive = (lmbda / 2) * (dolfin.tr(epsilon) ** 2) + mu * dolfin.tr(
    epsilon * epsilon
)

kappa = 1e3
psi_compress = kappa * (J * dolfin.ln(J) - J + 1)

psi = psi_passive + psi_compress + psi_active

P = dolfin.diff(psi, F)


ffun = dolfin.MeshFunction("size_t", mesh, 2)
ffun.set_all(0)

# Mark subdomains
fixed = dolfin.CompiledSubDomain("near(x[0], 0) && on_boundary")
fixed_marker = 1
fixed.mark(ffun, fixed_marker)

bcs = dolfin.DirichletBC(V, dolfin.Constant((0.0, 0.0, 0.0)), fixed)

weak_form = dolfin.inner(P, dolfin.grad(v)) * dolfin.dx
jacobian = jacobian = dolfin.derivative(
    weak_form,
    u,
    dolfin.TrialFunction(V),
)

problem = NonlinearProblem(F=weak_form, J=jacobian, bcs=bcs)
solver = NewtonSolver(comm=mesh.mpi_comm())
solver.hello_from_solver()
solver.solve(problem, u.vector())
dolfin.File("u.pvd") << u
