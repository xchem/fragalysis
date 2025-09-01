
# Using the Fragalysis REST API

The list of Fragalysis' REST API endpoints can be found at `<fragalysis url>/api`.

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


