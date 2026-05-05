
# Fragalysis

Fragalysis is a powerful app that can be used to visualise, analyse, and curate experimental and virtual fragment-screening data from inside your browser.

## Getting started

Crystallographic data are uploaded to Fragalysis via [XChem Align](https://xchem-align.readthedocs.io) using either the [production](https://fragalysis.diamond.ac.uk) or [staging](https://fragalysis.xchem.diamond.ac.uk) stacks. If you are new to Fragalysis, we recommend starting with the [**Fragalysis user guide**](user_guide) to familiarise yourself with the most common analysis tasks.

## Quick links:

- [**DLS Fragalysis Production stack**](https://fragalysis.diamond.ac.uk)
- [**DLS Fragalysis Staging stack**](https://fragalysis.xchem.diamond.ac.uk)
- [**fragalysis-app slack channel**](https://xchem-workspace.slack.com/archives/C02RCMA6S0Z)
- [**What's changed? (Release notes)**](changelog)
- [**XChemAlign documentation**](https://xchem-align.readthedocs.io/en/latest/USER-GUIDE.html)

---

# Documentation Pages

## Fragalysis User Guide
```{toctree}
:maxdepth: 1
user_guide.md
```

### Experimental Structures (LHS)
* {ref}`Browsing experimental data <browsing-experimental-data>`
* {ref}`Downloading experimental data <downloading-experimental-data>`
* {ref}`Curating experimental data <curating-experimental-data>`
* {ref}`Uploading assay measurements or computed scores <uploading-assays>`

### Computed Structures (RHS)
* {ref}`Browsing virtual compound sets <browsing-virtual>`
* {ref}`Curating virtual compound sets <curating-virtual>`
* {ref}`Uploading virtual compound sets <uploading-virtual>`

### Jupyter Notebooks

```{toctree}
:maxdepth: 1
notebooks.md
```

### Programmatic Interface (API)

```{toctree}
:maxdepth: 1
api.md
py_api.md
```

### Other Pages

```{toctree}
:maxdepth: 1
changelog.md
```