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
from fragalysis.requests import target_list
targets = target_list(stack="production", token=token)
```

The `token` keyword can be ommitted if only accessing public targets, and `stack` can be either "production", "staging" or the URL of another Fragalysis deployment.

### Download target

To get a list of target dictionaries accessible with an optional authentication token:

```
from fragalysis.requests import download_target
download_target(name=target_name, tas=target_access_string, token=token, stack="production", destination=".")
```

The `token` keyword can be ommitted the target is public, `stack` can be either "production", "staging" or the URL of another Fragalysis deployment, tas is the "Target Access String" or DLS proposal-session string (e.g. `lb32627-66`), the destination can be any path and is "." by default.

```{note}
The Fragalysis frontend may offer more options for target download than this API. Contributions to update the python API for feature parity are much appreciated.

The `download_target` method which will need updating is in https://github.com/xchem/fragalysis/blob/main/fragalysis/requests/download.py

The available POST request parameters to `/api/download_structures` can be seen in the JavaScript code for the frontend https://github.com/xchem/fragalysis-frontend/blob/staging/js/components/snapshot/modals/downloadStructuresDialog.js (see variables MAP_FILES, CRYSTALLOGRAPHIC_FILES, PERMALINK_OPTIONS, OTHERS)

Relevant developer contacts on github are @mwinokan, @kaliif, and @boriskovar-m2ms.
```

## Tracking experiment uploads

For the purpose of automated scraping you can use the `target_uploads` function to see if there have been any recent uploads:

```
uploads = target_uploads(statistics_only=True)
```

This returns a dictionary keyed by (target_name, target_access_string):

```
{
    ('A71EV2A', 'lb32627-66'): {
        'target_id': 31,
        'target_name': 'A71EV2A',
        'target_access_string': 'lb32627-66',
        'project_id': 1,
        'last_upload_index': 8,
        'last_upload_timestamp': datetime.datetime(2025, 10, 8, 12, 34, 0, 693173, tzinfo=datetime.timezone.utc)
    },
    ...
}
```

You can then check `last_upload_index` against your most recent download, or use `last_upload_timestamp` to determine if a fresh download is needed.

Then use the `download_target` function as described above.

## API reference

```{autodoc2-summary}
:renderer: myst

fragalysis.requests.download.target_list
fragalysis.requests.download.download_target
fragalysis.requests.compounds.get_target_compound_smiles
```
