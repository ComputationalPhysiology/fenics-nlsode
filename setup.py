import sys
import sysconfig
from pathlib import Path

from skbuild import setup

here = Path(__file__).parent
long_description = (here / "README.md").read_text()

setup(
    name="fenics-nlsode",
    python_requires=">=3.7.0",
    version="0.0.1",
    description="Coupled nonlinear solver and ode solver in FEniCS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ComputationalPhysiology/fenics-nlsode",
    author="Henrik Finsberg, Cécile Daversin-Catty",
    author_email="henriknf@simula.no",
    maintainer_email="henriknf@simula.no",
    license="MIT",
    keywords=["ODE", "solver", "system", "equations", "cuda"],
    install_requires=[
        "numpy",
        "pygoss",
        "gotran",
        "cppyy",
        "importlib-metadata;python_version<'3.8'",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "cbcbeat": ["cbcbeat"],
        "plot": ["matplotlib"],
        "dev": [
            "Sphinx",
            "black",
            "bump2version",
            "flake8",
            "ipython",
            "isort",
            "mypy",
            "pdbpp",
            "pip",
            "pre-commit",
            "pytest",
            "pytest-cov",
            "twine",
            "wheel",
        ],
        "docs": [
            "Sphinx",
            "myst_parser",
            "sphinx_book_theme",
            "sphinxcontrib-bibtex",
            "sphinx-math-dollar",
        ],
    },
    cmake_args=[
        "-DPython3_EXECUTABLE=" + sys.executable,
        "-DPython3_LIBRARIES=" + sysconfig.get_config_var("LIBDEST"),
        "-DPython3_INCLUDE_DIRS=" + sysconfig.get_config_var("INCLUDEPY"),
    ],
    packages=["nlsode"],
    package_dir={"": "python"},
    cmake_install_dir="python/nlsode/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
