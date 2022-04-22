#include <dolfin.h>
#include <nlsode/NewtonSolver.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <memory>
#include <vector>


namespace py = pybind11;

void init_NewtonSolver(py::module &m)
{

    // dolfin::NewtonSolver 'trampoline' for overloading virtual
    // functions from Python
    class PyNewtonSolver : public nlsode::NewtonSolver
    {
        using nlsode::NewtonSolver::NewtonSolver;

        // pybdind11 has some issues when passing by reference (due to
        // the return value policy), so the below is non-standard.  See
        // https://github.com/pybind/pybind11/issues/250.

        bool converged(const dolfin::GenericVector &r,
                       const dolfin::NonlinearProblem &nonlinear_problem, std::size_t iteration)
        {
            PYBIND11_OVERLOAD_INT(bool, nlsode::NewtonSolver, "converged", &r, &nonlinear_problem,
                                  iteration);
            return nlsode::NewtonSolver::converged(r, nonlinear_problem, iteration);
        }

        void solver_setup(std::shared_ptr<const dolfin::GenericMatrix> A,
                          std::shared_ptr<const dolfin::GenericMatrix> P,
                          const dolfin::NonlinearProblem &nonlinear_problem, std::size_t iteration)
        {
            PYBIND11_OVERLOAD_INT(void, nlsode::NewtonSolver, "solver_setup", A, P,
                                  &nonlinear_problem, iteration);
            return nlsode::NewtonSolver::solver_setup(A, P, nonlinear_problem, iteration);
        }

        void update_solution(dolfin::GenericVector &x, const dolfin::GenericVector &dx,
                             double relaxation_parameter,
                             const dolfin::NonlinearProblem &nonlinear_problem,
                             std::size_t iteration)
        {
            PYBIND11_OVERLOAD_INT(void, nlsode::NewtonSolver, "update_solution", &x, &dx,
                                  relaxation_parameter, nonlinear_problem, iteration);
            return nlsode::NewtonSolver::update_solution(x, dx, relaxation_parameter,
                                                         nonlinear_problem, iteration);
        }
    };

    // Class used to expose protected dolfin::NewtonSolver members
    // (see https://github.com/pybind/pybind11/issues/991)
    class PyPublicNewtonSolver : public nlsode::NewtonSolver
    {
      public:
        using NewtonSolver::converged;
        using NewtonSolver::solver_setup;
        using NewtonSolver::update_solution;
    };

    // dolfin::NewtonSolver
    py::class_<nlsode::NewtonSolver, std::shared_ptr<nlsode::NewtonSolver>, PyNewtonSolver,
               dolfin::Variable>(m, "NewtonSolver")
            .def(py::init<>())
            // .def(py::init([](const MPICommWrapper comm) {
            //     return std::unique_ptr<PyNewtonSolver>(new PyNewtonSolver(comm.get()));
            // }))
            // .def(py::init([](const MPICommWrapper comm,
            //                  std::shared_ptr<dolfin::GenericLinearSolver> solver,
            //                  dolfin::GenericLinearAlgebraFactory &factory) {
            //     return std::unique_ptr<PyNewtonSolver>(
            //             new PyNewtonSolver(comm.get(), solver, factory));
            // }))
            .def("solve", &nlsode::NewtonSolver::solve)
            .def("converged", &PyPublicNewtonSolver::converged)
            .def("solver_setup", &PyPublicNewtonSolver::solver_setup)
            .def("update_solution", &PyPublicNewtonSolver::update_solution)
            .def("linear_solver", &nlsode::NewtonSolver::linear_solver,
                 py::return_value_policy::reference)
            .def("hello_from_solver", &nlsode::NewtonSolver::hello_from_solver);
}


PYBIND11_MODULE(_nlsodecpp, m)
{
    m.doc() = "This is a Python bindings of C++ goss Library";
    m.def("hello", &hello, "Method for checking if goss compiled with OpenMP support");
    init_NewtonSolver(m);
}
