# Fragalysis

![documentation build](https://github.com/xchem/fragalysis/workflows/documentation%20build/badge.svg)

![RTD latest build](https://readthedocs.org/projects/fragalysis/badge/?version=latest&style=plastic)

![GitHub last commit](https://img.shields.io/github/last-commit/xchem/fragalysis)

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

## Related repositories
The Fragalysis Stack you find running in Kubernetes relies on a number of related
(and diverse) repositories. We've tried to capture references to all of them
below, in no particular order: -

**xchem respositories**

[fragalysis-package] : Logic that allows connection to the neo4j graph

[fragalysis-backend] : Django/REST Framework application

[fragalysis-frontend] : Django visual application (frontend)

[fragalysis-stack] : The build logic that combines the backed and frontend
to create the container image

[fragalysis-api] : Command-line API utilities

[fragalysis-keycloak] : A specialised build of keycloak to provide a custom login theme

[fragalysis-ispyb-target-access-authenticator] : Code for the container image that acts
as an interface to ISPyB, yielding Target Access Strings based on username

[fragalysis-mock-target-access-authenticator] : A "mock" ISPyB authenticator
(providing results based on a config file)

[fragalysis-stack-kubernetes] : Ansible playbooks for application deployment and management

[fragalysis-stack-behaviour-tests] : Basic gherkin-based behaviour tests for the stack API

[xchem-align] : Tools to generate input data for Fragalysis

[docker-neo4j] : Custom neo4j image providing built-in S3 bucket bulk-loading

**3rd-party respositories (Informatics Matters)**

There are also a number of 3rd-party repositories that provide facilities for
the Fragalysis Stack application: -

[squonk2-data-manager] (`PRIVATE`) : The Squonk2 Data Manager
(a private repository and container image)

[squonk2-account-server] (`PRIVATE`) : The Squonk2 Account Server providing
accounting and billign services (a private repository and container image)

[squonk2-data-manager-ui] : The Squonk2 UI

[squonk2-data-manager-jupyter-operator] : The Squonk2 Jupyter Notebook operator
(launches notebooks)

[squonk2-data-manager-job-operator] : The Squonk2 Job operator
(launches Jobs)

[squonk2-fragmenstein] : Squonk2 JOb defintions used by the Fragalysi Stack

>   Numerous other respositories exist for Job execution etc.
    For inmformatics Matters any respository
    that has the topic tag `squonk2` or `squonk2-jobs` might be relevant.

**Fragmentation**

There is also the fragmentation logic that is used to compile the underlying neo4j
database CSV files. These processes rely on access to substabntial computing resources -
typically kubernetes or slurm: -

[fragmentor] (Informatics Matters)
: Standardisation, fragmentation and combination graph logic (and playbooks)

[fragmentor-k8s-orchestration] (Informatics Matters)
: Ansible playbooks for the Kubernetes-based execution of fragmentor Playbooks

---

[squonk2-fragmenstein]: https://github.com/InformaticsMatters/squonk2-fragmenstein
[squonk2-data-manager-job-operator]: https://github.com/InformaticsMatters/squonk2-data-manager-job-operator
[squonk2-data-manager-jupyter-operator]: https://github.com/InformaticsMatters/squonk2-data-manager-jupyter-operator
[squonk2-data-manager-ui]: https://github.com/InformaticsMatters/squonk2-data-manager-ui
[squonk2-account-server]: https://gitlab.com/informaticsmatters/squonk2-account-server
[squonk2-data-manager]: https://gitlab.com/informaticsmatters/squonk2-data-manager
[fragmentor-k8s-orchestration]: https://github.com/InformaticsMatters/fragmentor-k8s-orchestration
[fragmentor]: https://github.com/InformaticsMatters/fragmentor
[docker-neo4j]: https://github.com/xchem/docker-neo4j
[fragalysis-stack-behaviour-tests]: https://github.com/xchem/fragalysis-stack-behaviour-tests
[fragalysis-mock-target-access-authenticator]: https://github.com/xchem/fragalysis-mock-target-access-authenticator
[fragalysis-stack-kubernetes]: https://github.com/xchem/fragalysis-stack-kubernetes
[fragalysis-ispyb-target-access-authenticator]: https://github.com/xchem/fragalysis-ispyb-target-access-authenticator
[fragalysis-api]: https://github.com/xchem/fragalysis-api
[fragalysis-backend]: https://github.com/xchem/fragalysis-backend
[fragalysis-frontend]: https://github.com/xchem/fragalysis-frontend
[fragalysis-keycloak]: https://github.com/xchem/fragalysis-keycloak
[fragalysis-package]: https://github.com/xchem/fragalysis-package
[fragalysis-stack]: https://github.com/xchem/fragalysis-stack
[readthedocs]: https://app.readthedocs.org/dashboard/
[sphinx]: https://www.sphinx-doc.org/en/master
[xchem-align]: https://github.com/xchem/xchem-align
