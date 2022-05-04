//#include <dolfin.h>
#include <dolfin/nls/NewtonSolver.h>
namespace nlsode
{

class NewtonSolver : public dolfin::NewtonSolver
{
  public:
    void hello_from_solver();
    // std::pair<std::size_t, bool> solve(dolfin::NonlinearProblem &nonlinear_problem,
    //                                    dolfin::GenericVector &x)
    // {
    //     std::cout << "Hello world\n";
    //     return std::make_pair(1, true);
    // }
};

} // namespace nlsode

void hello();
