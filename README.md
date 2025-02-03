# Fragalysis

![documentation build](https://github.com/xchem/fragalysis/workflows/documentation%20build/badge.svg)

The "start here" repository for the Fragalysis Stack application.
This repository (which is currently **UNDER CONSTRUCTION**) will be used
as a 'base' for all documentation relating to the application.

>   This replaces the original fragalysis repository, which was responsible for the
    RDKit-based Python tools for analysis of protein-ligand interactions.
    The original repository has been renamed and can now be found in the
    [fragalysis-package] repository.

The repository is compatible with ReadTheDocs and you can find the latest documentation
(built from the most recent changes on this repository's `main` branch) on [ReadTheDocs] at
https://fragalysis.readthedocs.io/en/latest/.

Stable documentation (built from the most recent tag in this repository) can be found at
https://fragalysis.readthedocs.io/en/stable/.

## Local development
To compile the documentation, which is based on [Sphinx],
start with a Python environment (ideally Python 3.12, as that's the version used by
ReadTheDocs and the GitHub CI workflow) and install the dependencies: -

    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip

    pip install -r requirements.txt

Then, to build the HTML documentation, run the following command: -

    sphinx-build docs/source/ docs/build/

The resulting `index.html` will be in the `docs/build/` directory.

---

[fragalysis-package]: https://github.com/xchem/fragalysis-package
[readthedocs]: https://app.readthedocs.org/dashboard/
[sphinx]: https://www.sphinx-doc.org/en/master
