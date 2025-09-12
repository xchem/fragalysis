
# Using the Fragalysis Python API

A work in progress Python package to interface with the Fragalysis web service via the [REST API](api) is available at [github.com/xchem/fragalysis](https://github.com/xchem/fragalysis).

## Installation

Install using pip:

```
git clone https://github.com/xchem/fragalysis
cd fragalysis
pip install --user -e .
```

## Usage

### Get list of targets

To get a list of target dictionaries accessible with an optional authentication token:

```
from fragalysis.requests.download import target_list
targets = target_list(stack="production", token=token)
```

The `token` keyword can be ommitted if only accessing public targets, and `stack` can be either "production", "staging" or the URL of another Fragalysis deployment.

### Download target

To get a list of target dictionaries accessible with an optional authentication token:

```
from fragalysis.requests.download import download_target
download_target(name=target_name, tas=target_access_string, token=token, stack="production", destination=".")
```

The `token` keyword can be ommitted the target is public, `stack` can be either "production", "staging" or the URL of another Fragalysis deployment, tas is the "Target Access String" or DLS proposal-session string (e.g. `lb32627-66`), the destination can be any path and is "." by default.

## API reference

```{autodoc2-summary}
:renderer: myst

fragalysis.requests.download.target_list
fragalysis.requests.download.download_target
```
