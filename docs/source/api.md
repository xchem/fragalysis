
# Using the Fragalysis REST API

The list of Fragalysis' REST API endpoints can be found at `<fragalysis url>/api`.

## Target Access Strings

Fragalysis Targets are associated with _proposals_, also referred to as
**Target Access Strings** (TAS for short). Proposals, and the individuals who are
assigned to them, are maintained on a Diamond-managed database.
Fragalysis uses an [Authenticator] service to query the database to enforce rules
relating to what people can _see_ and contribute to (modify).
Some proposals are _open_, which means that Targets associated with these are visible
to everyone, even those who are not logged-in (authenticated).
`lb18145-1` is one such proposal.

A TAS consists of three items: a two-letter _code_, a proposal _number_,
and a hyphen followed by a _visit_ (_session number_). It is only valid if all three
are present. Depending on how it's been configured Fragalysis may also limit the codes
that can be used, although the use of `lb` and `sw` are commonly permitted.

So, what you see (and what you can edit) is controlled by your proposal membership.

### Seeing your TAS set

If you are unsure why you are not seeing material that you think you should be able to
Fragalysis exposes a REST API endpoint that can be used to see your TAS membership.

As the membership database may not always be available the authenticator caches
each user's TAS set as it is collected. So, when the database is offline or
communication errors are encountered, the authenticator returns your cache.
the cache is nor persisted and wil be lost, for example, if the application
is rebooted.

### Understanding the authenticator

If you are still unsure about why you are not a member of a particular TAS,
and you are sure you should be, you can inspect the authenticator, which will
provide a lot of statistical information relating to its internal operation,
but also about it's connection to the proposal database.

The authenticator exposes a REST API endpoint to do this, which produces a YAML-like
text response. You will need to provide an _access key_, which is used to prevent
unauthorised access.

Assuming you have the key, authentication statistics can be obtained using a **GET**
from the exposed endpoint. In the following example the key is `4pp4CmJP2wCz2EiGgCctG`
(which is not the actual key of course - you will need to contact the Fragalysis
administrators to get the real key). Here we use [httpie] (and `curl`)
to retrieve the statistics: -

    STATS_KEY=4pp4CmJP2wCz2EiGgCctG

    http https:///ta-authenticator.xchem.diamond.ac.uk X-TAAStatsKey:${STATS_KEY}

    curl https:///ta-authenticator.xchem.diamond.ac.uk -H X-TAAStatsKey:${STATS_KEY}

The response is quite detailed, and many parts of it will only make sense
if you understand the inner-workings of the authenticator.

The **auth section** provides information about the type (and version) of authenticator
that's being used: -

```yaml
auth:
  kind: ISPYB
  name: XChem Python FastAPI TAS Authenticator
  version: 1.4.0
```

The **code_set section** lists the restricted set of proposal codes that are
in use. If this list is empty (`[]`) as it is in this example any code is
permitted by the authenticator: -

```yaml
code_set: []
```

>   The code set may be further limited within Fragalysis, which has its own
    additional filter. Typically `lb` and `sw` will be permitted.

The **ping section** indicates the health of the database connection. The database
is responding correctly if `status` is `OK`. The age of the status can also be seen
along with the dates and times the status changed. In the following example
the database connection was last checked `20 seconds` ago, it is reported as `OK`,
and it has been OK for 2 hours (since `10:34` UTC). Before 10:34 you can assume the
status (database connection) was not OK.

```yaml
ping:
  age: 20 seconds
  status: OK
  status_change_age: 2 hours
  status_change_timestamp: '2025-10-10T10:34:25.537069+00:00'
```

>   While the connection is OK the authenticator can make new proposal queries. If
    it is not OK the authenticator relies on any pre-collected and cached results.
    Results are cached for a user, but the database is only queried when the user
    is actively using Fragalysis.

The **user section** displays simplified results for each user.
If your user ID is not in the `users -> user_stats` list then proposals have not
been collected for you. In this example user `abc12345` is associates with 12 TAS
that were collected from the database at 10:34 (UTC): -

```yaml
users:
  user_stats:
  - username: abc12345
  - tas_count: 12
  - collected: '2025-10-10T10:34:25.537069+00:00'
```

If there are no users known to the authenticator the list will be empty: -

```yaml
users:
  user_stats: []
```

[authenticator]: https://github.com/xchem/fragalysis-ispyb-target-access-authenticator
[httpie]: https://httpie.io

## Using endpoints from python scripts

Fragalysis API can be accessed from Python scripts directly but there are a couple of things to look out for. Most of the endpoints require authentication. To obtain the authentication token, first log into Fragalysis and find it from the UI or visit the `api/token` endpoint. Cross-site scripting prevention can also sometimes cause problems. To use the endpoints from python scripts, you need to make sure the authentication token and CSRFtoken are set and correct.

```python

import requests
from urllib.parse import urljoin

LANDING_PAGE_URL = '/viewer/react/landing/'

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

```

User agent string does not need a refresh with every browser version, but it needs to be more or less up to date.

Use the session object so that the server can recognize you between the requests:

```python

landing_page_url = urljoin(fragalysis_base_url, LANDING_PAGE_URL)

session.headers.update({
    'User-Agent': USER_AGENT,
    'Referer': landing_page_url,
    'Referrer-policy': 'same-origin',
})

session.get(landing_page_url)

```

GET request to main page usually sets the csrftoken, but in case it doesn't:

```python
csrftoken = session.cookies['csrftoken']
session.headers.update({
    'X-CSRFToken': csrftoken,
})

```

If the endpoint requires authentication (as most endpoints do) add the authentication token to cookies:

```python
session.cookies.update({
    'sessionid': auth_token,
})

```
You are now ready to make a request to the desired endpoint.


## Endpoints

### `/api/upload_target_experiments/`
This endpoint lets you view dataset (experiment) info. If used with experiment ID, `/api/upload_target_experiments/<id>` the response contains information only about the selected experiment, othewise the list of all experiments is returned. The single experiment object contains the following fields:

- id: experiment ID
- code: experiment code
- pdb_info: downloadable link of pdb info file
- pdb_info_source_file: pdb info souce file path in Diamond file system
- mtz_info: downloadable link of mtz info file
- mtz_info_source_file: mtz info souce file path in Diamond file system
- cif_info: downloadable link of cif info file
- cif_info_source_file: cif info souce file path in Diamond file system
- map_info: list of map info files
- map_info_source_files: list of map info souce file paths in Diamond file system
- type: type code
- pdb_sha256:
- prefix_tooltip: tooltip shown on hover in the frontend
- code_prefix: prefix prepended to observation shortcodes
- cchalf_high_res_shell:
- cchalf_overall:
- completeness_high_res_shell:
- completeness_overall:
- crystal_mounting_result:
- data_collection_date:
- data_collection_outcome:
- date_model_last_updated:
- date_status_updated:
- date_refined:
- dimple_rfree:
- dimple_rwork:
- experiment_comments:
- experiment_status:
- experiment_type:
- experiment_start_date:
- final_compound_concentration_mm:
- high_resolution:
- isig_i_overall:
- isig_i_high_res_shell:
- library:
- library_plate:
- ligand_confidence:
- ligand_correlation_coefficient:
- modelled_smiles:
- panddarun:
- pdb_code:
- processing_pipeline:
- refinement_comment:
- refinement_rfree:
- refinement_rwork:
- soakdb_entry:
- soaking_time:
- source_well:
- space_group:
- unit_cell_dimensions:
- experiment_upload: experiment upload ID
- status: status code
- xtalform: crystalform ID
- refinement_outcome:
- model_last_updated: user ID
- refined_by: user ID
- compounds: the list of compound IDs connected to this experiment


### `/api/download_structures/`

This endpoint allows downloading target data from Fragalysis. Working with this endpoint requires two request: the first one, POST with the payload detailing the data to return compiles the requested data and compresses it into a zipfile. The response returned from POST contains an URL to the file which can then be fetched with GET request to the same endpoipnt. The POST request payload accepts the following parameters for fine-tuning the response content:

- target_name: mandatory. Expects targets `title` field, not `display_name`
- target_access_string: mandatory. Target access string in format `lbXXXXX-X`
- proteins: default '' (empty string, download all observations in target). Comma separated list of observation shortcodes. If used, only the selected observations will be downloaded.
- all_aligned_structures: default True. Downloads 7 file types:
  - `aligned_files/*.pdb`
  - `aligned_files/*_apo.pdb`
  - `aligned_files/*_apo-solv.pdb`
  - `aligned_files/*_apo-desolv.pdb`
  - `aligned_files/*_ligand.pdb`
  - `aligned_files/*_ligand.sdf`
  - `aligned_files/*_ligand.smi`
- pdb_info: default False. Downloads `crystallographic_files/*.pdb`
- cif_info: default False. Downloads `crystallographic_files/*.cif`
- mtz_info: default False. Downloads `crystallographic_files/*.mtz`
- diff_file: default False. Downloads `aligned_files/*_diff.ccp4`
- event_file: default False. Downloads`aligned_files/*_event.ccp4`
- sigmaa_file: default False. Downloads`aligned_files/*_sigmaa.ccp4`
- map_info: default False. Downloads `crystallographic_files/*.ccp4`
- single_sdf_file: default False. Combines all `aligned_files/*_ligand.sdf` files into a single SDF file
- metadata_info: default False. Compile and download `metadata.csv`
- static_link: default False. This parameter is ignored.
- file_url: default '' (empty string). Download previoulsy compiled download. If included, all other parameters are ignored and only the existing zipfile is downloaded
- trans_matrix_info: default False. Download `neighbourhood_transforms.yaml`, `conformer_site_transforms.yaml` and `reference_structure_transforms.yaml`
