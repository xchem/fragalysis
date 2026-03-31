# Fragalysis

![PyPI - Version](https://img.shields.io/pypi/v/xchem-fragalysis)

![documentation build](https://github.com/xchem/fragalysis/actions/workflows/documentation-build.yaml/badge.svg)
![release](https://github.com/xchem/fragalysis/actions/workflows/release.yaml/badge.svg)

![RTD latest build](https://readthedocs.org/projects/fragalysis/badge/?version=latest&style=plastic)

![GitHub last commit](https://img.shields.io/github/last-commit/xchem/fragalysis)

The "start here" repository for the Fragalysis Stack application.
This repository (which is currently **UNDER CONSTRUCTION**) will be used
as a 'base' for all documentation relating to the application.

>   This replaces the original fragalysis repository, which was responsible for the
    RDKit-based Python tools for analysis of protein-ligand interactions.
    The original repository has been renamed and can now be found in the
    [fragutils] repository.

The repository is compatible with ReadTheDocs and you can find the latest documentation
(built from the most recent changes on this repository's `main` branch) on [ReadTheDocs] at
https://fragalysis.readthedocs.io/en/latest/.

Stable documentation (built from the most recent tag in this repository) can be found at
https://fragalysis.readthedocs.io/en/stable/.

## XChem repositories
A significant amount of our work resides in public GitHub repositories in the
`XChem` organisation. A growing list of all the repositories that represent
our work can be found in the **Related repositories** section below. We also rely on a
number of _external_ repositories (those not managed by us directly). Importantly,
when we find that the material in such a repository becomes crucial to our work we
**SHOULD** consider *fork* it to `XChem`. Forking allows us to: -

- Preserve content
- Adopt our own development processes, which include: -
  - A consistent release mechanism
  - Consistent package naming (PyPI packages all begin `xchem-` for example)
  - Use of linting, formatting, and test tools that we like
- Improve stability (we like working with static *tagged* references)

In `xchem` we tend to follow a trunk-based development strategy that we explain in
our [trunk-based-development] repository. It's provides us with a centrally-defined
set of policies with accompanying documentation on its [wiki] - a place
where we provide guidance, some advanced topics, and development inspiration.

**Working on codes that's not in XChem?**

If you are using code that we don't own (manage) we **MUST** consider forking the
repository into `XChem`, applying our development process, tagging it when important
changes are available, and asking others to switch to using our repository and the
packages it produces.

## Local development
To compile the documentation, which is based on [Sphinx],
start with a Python environment (ideally Python 3.12, as that's the version used by
ReadTheDocs and the GitHub CI workflow) and install the dependencies: -

    pip install uv
    uv venv
    source .venv/bin/activate
    pip install -r rtd-requirements.txt

Then, to build the HTML documentation, run the following command: -

    sphinx-build docs/source/ docs/build/

The resulting `index.html` will be in the `docs/build/` directory.

## Related repositories
The Fragalysis Stack you find running in Kubernetes relies on a number of related
(and diverse) repositories. We've tried to capture references to all of them
below, in no particular order: -

**xchem repositories**

[trunk-based-development] : A repository for development guidance

[fragutils] : Logic that allows connection to the neo4j graph

[fragalysis-backend] : Django/REST Framework application

[fragalysis-frontend] : Django visual application (frontend)

[fragalysis-stack] : The build logic that combines the backed and frontend
to create the container image

[fragalysis-api] : Command-line API utilities

[fragalysis-database] : A reference PostgreSQL database image (with extras)

[fragalysis-keycloak] : A specialised build of keycloak to provide a custom login theme
deprecated

[fragalysis-ispyb-target-access-authenticator] : Code for the container image that acts
as an interface to ISPyB, yielding Target Access Strings based on username

[fragalysis-mock-target-access-authenticator] : A "mock" ISPyB authenticator
(providing results based on a config file)

[fragalysis-target-access-authenticator-python-client] : A Python client for the authenticator

[fragalysis-rdkit-cartridge-pgvector-debian] : An extension to the underlying database
image (informaticsmatters/rdkit-cartridge-debian) that adds PG-Vector utilities

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

[squonk2-fragmenstein] : Squonk2 Job defintions used by the Fragalysi Stack

>   Numerous other respositories exist for Job execution etc.
    For inmformatics Matters any respository
    that has the topic tag `squonk2` or `squonk2-jobs` might be relevant.

[docker-volume-replicator] : Replicates volumes (used for media)

[bandr] : PostgreSQL backup and recovery container images

**Fragmentation**

There is also the fragmentation logic that is used to compile the underlying neo4j
database CSV files. These processes rely on access to substabntial computing resources -
typically kubernetes or slurm: -

[fragmentor] (Informatics Matters)
: Standardisation, fragmentation and combination graph logic (and playbooks)

[fragmentor-k8s-orchestration] (Informatics Matters)
: Ansible playbooks for the Kubernetes-based execution of fragmentor Playbooks

---

[bandr]: https://github.com/InformaticsMatters/bandr
[docker-volume-replicator]: https://github.com/InformaticsMatters/docker-volume-replicator
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
[fragalysis-target-access-authenticator-python-client]: https://github.com/xchem/fragalysis-target-access-authenticator-python-client
[fragalysis-stack-kubernetes]: https://github.com/xchem/fragalysis-stack-kubernetes
[fragalysis-ispyb-target-access-authenticator]: https://github.com/xchem/fragalysis-ispyb-target-access-authenticator
[fragalysis-rdkit-cartridge-pgvector-debian]: https://github.com/xchem/fragalysis-rdkit-cartridge-pgvector-debian
[fragalysis-api]: https://github.com/xchem/fragalysis-api
[fragalysis-database]: https://github.com/xchem/fragalysis-database
[fragalysis-backend]: https://github.com/xchem/fragalysis-backend
[fragalysis-frontend]: https://github.com/xchem/fragalysis-frontend
[fragalysis-keycloak]: https://github.com/xchem/fragalysis-keycloak
[fragutils]: https://github.com/xchem/fragutils
[fragalysis-stack]: https://github.com/xchem/fragalysis-stack
[readthedocs]: https://app.readthedocs.org/dashboard/
[sphinx]: https://www.sphinx-doc.org/en/master
[trunk-based-development]: https://github.com/xchem/trunk-based-development
[xchem-align]: https://github.com/xchem/xchem-align
[wiki]: https://github.com/xchem/trunk-based-development/wiki
