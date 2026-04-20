# Fragalysis User Guide

```{toctree}
:maxdepth: 1
```

Fragalysis is a web-based platform for the visualisation, comparison, and analysis of fragment-bound protein crystal structures, assay measurements, and follow-up virtual ligand screens. It can effectively be divided into:

**Experimental** fragment screening data processed via [XChem Align](https://xchem-align.readthedocs.io) and uploaded to Fragalysis, curated and downloaded via the **"left-hand side" (LHS)** of Fragalysis.

**Computed** follow-up designs from virtual compound sets uploaded to Fragalysis, curated and downloaded via the **"right-hand side" (RHS)** of Fragalysis.

---

## Getting started

Fragalysis can be used to explore data in a number of ways:

**Experimental Structures (LHS)**

* [Browsing Experimental data](#browsing-experimental-data)
* [Curating Experimental data](#curating-experimental-data)
* [Uploading assay measurements or computed scores](#uploading-assays)

**Computed Structures (RHS)**
* [Browsing virtual compound sets](#browsing-virtual)
* [Curating virtual compound sets](#curating-virtual)
* [Uploading virtual compound sets](#uploading-virtual)

**Jupyter Notebooks**
* [Jupyter Notebooks in Fragalysis](notebooks.md)

**Programming Interface (API)**
* [Using the Fragalysis REST API](api.md)
* [Using the Fragalysis Python API](py_api.md)

---

### Navigating the homepage

Navigating to the Fragalysis homepage for the first time you will be prompted to log in with your FedID. This will allow you to view the "private targets" associated with your Diamond user account, alongside public and legacy targets:

```{image} _static/media/homepage_login.png
:width: 1000px
:alt: Fragalysis login page
```

### The Fragalysis "viewer" interface
The Fragalysis viewer has been customised for fragment screening workflows, is fully interactive and runs directly in your browser. When opening a target, you will be presented with an interface that allows you to interact with and curate data:

<img src="_static/media/fragalysis.png" alt="lhs" width="1000px">

- **Share/snapshot** this allows you to create and share a permanent link to your exact Fragalysis state
- **Tags** This is how you can control which hits are visible by sites and other categories
- **LHS / Hits** Here you can navigate all the hits and add visualisations to them (The Tags panel also belongs to the LHS)
- The visualisation buttons are shared also with virtual hits (RHS) and work as follows:
   - **A**ll : show ligand in (CPK), protein side chains (lines), and interactions.
   - **L**igand: Ligand (CPK)
   - **P**rotein: Protein side chains (lines)
   - Intera**c**tions: Interactions
   - **S**urface: Electrostatic surface of the protein
   - Electron **D**ensity: Experimental electron density
   - **V**ectors: Possible vectors for elaboration
 
### Controlling the 3D viewer
Fragalysis uses NGL viewer under the hood to visualise 3D models, inspect binding sites, and compare multiple structures at once. It can be easily controlled with mouse and keyboard inputs:

| Key / Mouse action        | Effect                                           |
|---------------------------|--------------------------------------------------|
| scroll                    | Zoom scene                                       |
| scroll + Ctrl             | Move near clipping plane                         |
| scroll + Shift            | Move near clipping plane and far fog             |
| scroll + Alt              | Change isolevel of isosurfaces                   |
| drag right                | Pan / translate scene                            |
| drag middle               | Zoom scene                                       |
| drag left                 | Rotate scene                                     |
| drag + Shift + right      | Zoom scene                                       |
| drag left + right         | Zoom scene                                       |
| drag + Ctrl + right       | Pan / translate hovered component                |
| drag + Ctrl + left        | Rotate hovered component                         |
| click pick (middle)       | Auto view picked component element               |
| hover pick                | Show tooltip for hovered component element       |
| i                         | Toggle stage spinning                            |
| k                         | Toggle stage rocking                             |
| p                         | Pause all stage animations                       |
| r                         | Reset stage auto view                            |

### Geometric filtering

Geometric filtering allows you to limit hits based on their position in 3D space. When you click any structure in the NGL Viewer, a green semi-transparent sphere will appear. After clicking **Apply** in the **Radius selection** dialog, only hits that intersect with the sphere will be shown in the hit navigator.

<img src="_static/media/FilteringSphere.png" alt="lhs" width="600px">

This feature is **ON** by default and can be toggled in the Advanced Search dialog. If you turn it off, any existing geometric filtering is cleared and no spatial filtering will be applied.

<img src="_static/media/AdvancedSearchDialog.png" alt="lhs" width="600px">

---

(browsing-experimental-data)=
## Browsing experimental data (LHS)

The left-hand-side (LHS) user interface of Fragalysis allows you to select experimental data for display, download, and computation.

There are three panels Tag Details, Hit Navigator, and Snapshot:

### Tag Details

Tags are user-defined labels used to organise, filter, and annotate structures and fragments within Fragalysis. They provide a flexible way to group related data and share interpretation without modifying the underlying experimental data. This section details how tags can be used to filter experimental data. To add and edit tags see the [curating experimental (LHS) data](#curating-experimental-data) page.

All tags assigned to left-hand side data can be managed in this panel:

<img src="_static/media/lhs_tag_panel.png" alt="lhs" width="600px">

Select tags to show datasets assigned to that tag in the [Hit navigator](#hit-navigator). The union / intersection toggle at the top of the page can be used to determine the behaviour when multiple tags are selected:

- **Union**: Display datasets that are tagged with **at least one** of the selected tags
- **Intersection**: Display datasets that are tagged with **all** of the selected tags

| Control | Description |
|--------|-------------|
| **SHOW UNTAGGED HITS** | Displays only datasets that do not have any tags assigned. Useful for identifying new or unreviewed fragment hits. |
| **SHOW ALL HITS** | Displays all datasets, ignoring the current tag selection. Overrides any active tag filters. |
| **SELECT ALL TAGS** | Selects all available tags in the tag list. Does not automatically select hits in the hit navigator. |
| **SELECT HITS** (per tag) | Activates selection checkboxes for all datasets associated with the chosen tag. Useful for bulk operations on tagged datasets. |

(hit-navigator)=
### Hit navigator

The Hit Navigator is the primary panel in Fragalysis for browsing, filtering, and selecting fragment screening hits associated with a target. It controls which datasets are loaded into the structure viewer and provides tools for organising hits using tags and metadata.

<img src="_static/media/lhs_hit_panel.png" alt="lhs" width="600px">

#### LHS "poses" and "observations"

Ligands from experimental datasets are known as **observations** are grouped into **poses**. **Poses** are named after and take their behaviour from their **main observation**.

**Poses** and **observations** have the following interface:

<img src="_static/media/lhs_pose.png" alt="lhs" width="600px">

#### Display data in the 3D viewer

<img src="_static/media/lhs_3d_buttons.png" alt="lhs" width="200px">

The **[A][L][P][C][S][D][V]** buttons can be used to activate various representations of the observation in the 3D NGL viewer:

- **[A]**: shortcut to activate **[L][P][C]**
- **[L]**: **L**igand (ball and stick)
- **[P]**: **P**rotein sidechains (lines)
- **[C]**: Intera**C**tions
- **[S]**: **S**urface (coloured by electrostatics)
- **[D]**: Electron **D**ensity maps
- **[V]**: Expansion **V**ectors

#### What decides which hits are shown?

The hit navigator follows these key rules to determine which datasets are shown:

1. All datasets displayed in the 3d viewer are shown
1. Datasets from active tags are shown
1. If a search string is present, only observations matching that string are shown

#### Searching for specific hits

The search bar can be used to search for specific hits:

<img src="_static/media/lhs_search.png" alt="lhs" width="300px">

Your search query will be matched against the following fields:

- Observation shortcode
- Compound aliases
- Compound ID

This can be customised by clicking on the magnifying glass icon.

See also [Creating direct URLs to specific views](#creating-urls)

### Snapshots

Snapshots are saved views of the current analysis state, allowing you to quickly return to a specific set of selected hits and visualisation settings, and making it easy to share or revisit a particular analysis.

```{image} _static/media/snapshot.png
:width: 600px
:alt: snapshot window
```
(creating-urls)=
### Creating direct URLs to specific views

To link to specific datasets within a target, the following syntax is supported:

#### Specifying the target and proposal

The following URL takes you to the target with:

- name: `A71EV2A`
- target access string (tas): `lb32627-66`:

[https://fragalysis.diamond.ac.uk/viewer/react/preview/target/A71EV2A/tas/lb32627-66](https://fragalysis.diamond.ac.uk/viewer/react/preview/target/A71EV2A/tas/lb32627-66)


#### Using the `direct` URL syntax

You can also create URLs that display specific datasets. To use this functionality you have to use this base URL including the `direct` command:

```
https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/
```
**Examples**

***e.g. showing observations with ligands where compound alias contains substring `ASAP`:***

[https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP/L](https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP/L)

- `target/A71EV2A`: specifies the target name
- `tas/lb32627-66`: specifies the target access string
- `compound/ASAP/L`: shows the ligand (`L`) representation for all `compound` aliases containing `ASAP`

***e.g. showing observations with ligands where compound alias is exactly `ASAP-0016733-001`:***

[https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP-0016733-001/L/exact](https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP-0016733-001/L/exact)

- `target/A71EV2A`: specifies the target name
- `tas/lb32627-66`: specifies the target access string
- `compound/ASAP-0016733-001/L/exact`: shows the ligand (`L`) representation for exact `compound` aliases match `ASAP-0016733-001`

---

(curating-experimental-data)=
## Curating experimental data (LHS)

[XChemAlign](https://xchem-align.readthedocs.io) transforms crystallographic data into a biological reference frame. This involves matching ligand neighbourhoods across crystalforms, assemblies, and chains onto a appropriate reference structures. This process generates various _sites_ which make their way into Fragalysis via tags. All tag information is also included in the `metadata.csv` in any Fragalysis download.

<img src="_static/media/xca_transformation_figure.png" alt="xca_transformation_figure" width="800px">

### Working with XCA-assigned sites/tags

The main XCA-assigned site is called a _Canonical Site_ and effectively clusters ligands. When you first upload a target to Fragalysis all CanonSite tags will have an auto-generated name and colour. See CanonSite 2: `2 - c0692/D/304/1` in the screenshot below. The yellow `2` in the hit navigator corresponds to this canonical site. 

<img src="_static/media/lhs_canonsite_highlight.png" alt="lhs_canonsite_highlight" width="600px">

#### Editing tags

The colour, name, and visibility of the site can be changed in the `Edit Tags` dialog. 

<img src="_static/media/edit_tags.png" alt="edit_tags" width="800px">

```{note}
N.B. you must be logged in and on the UAS proposal to make any changes to a Fragalysis target.
```

#### Changing site assignments

If you disagree with the clustering from XCA you can change the assigned sites via the observation dialog (click on the observation count to open):

<img src="_static/media/change_xca_site.png" alt="change_xca_site" width="800px">

### Adding "Curator" tags

For additional annotation of structures _Curator Tags_ can be created via the `Edit Tags` window. Select `Other -- new tag --` from the dropdown. These tags can be added to observations in the tag navigator:

<img src="_static/media/add_tag.png" alt="add_tag" width="800px">

### Indicating merging hypotheses

For _Fast Forward Fragments_ it is required to create one _Curator Tag_ for each group of fragments that you wish to explore merging. These can often just be all hits in the pockets of interest.

### Indicating experimental / model quality

The experimental / model quality can be indicated using the traffic light system:

<img src="_static/media/traffic_lights.png" alt="traffic_lights" width="600px">

Each observation will have a `Main Status`, it should be decided in your project who has the final say on this, typically there is one main data owner / structural biologist. All other members are recommended to only add `Peer Reviews`. These not only have a status, but also allow for a comment.

---

(uploading-assays)=
## Uploading assay measurements or computed scores (LHS)

Fragalysis supports annotation of experimental data with text or numeric scores that are linked either to compound codes or observation short codes.

```{warning}
Do not upload any assay data to a public target that is confidential! Measurements against compounds that do not (yet) have structures will still be accessible to authorised API users.
```

### Creating the assay data CSV

Create a CSV with:

- one identifier column, containing either compound codes or observation short codes
- as many text/numeric columns as you want
- The data type of columns can optionally be specified by an additional row containing `text`, `int`, or `float`

<img src="_static/media/assay_data_csv.png" alt="assay_data_csv" width="300px">

Please note that CDD data can be exported as a CSV and often uploading with minimal manual modification.

### Uploading

- Log in and open your target of interest
- Select `Assay data upload` from the menu
- Complete the form:

<img src="_static/media/assay_data_form.png" alt="assay_data_form" width="300px">

### Modifying data type of existing data column

Use the `/api/activity_data_curation/` endpoint to change data types of previously uploaded scores

---

(browsing-virtual)=
## Browsing virtual compound sets (RHS)

### Overview of the RHS interface

The right hand side (RHS) is where follow-up designs and their virtual hits are navigated. Follow-up designs are grouped into **compound sets**, corresponding to each SDF that was uploaded (See [Uploading compound sets to the RHS](#uploading-virtual)).

### Inspirations

The `F` button on each compound can be used to bring up a modal with the experimental hits used as **inspirations** / references for the compound design. The same LHS visualisation buttons are available to superimpose the inspiration hit with the follow-up design. When an experimental dataset is displayed, all virtual designs referencing that ligand will have their `F` icon active. 

<img src="_static/media/rhs_curation.png" alt="rhs" width="900px">

### Sorting and filtering

Clicking on the **filter** <img src="_static/media/filter_button.png" alt="filter" width="30px"> icon allows you to sort and filter the compounds by properties present in the uploaded set. Typically you will find scores such as *energy_score* representing computed binding energy, *distance_score* representing RMS distance to the fragment inspirations, and *score_inspiration* which may indicate how well the fragments references have been recapitulated:

<img src="_static/media/rhs_filter.png" alt="rhs" width="780px">

---

(curating-virtual)=
## Curating virtual compound sets (RHS)

(colours-painting)=
### Colours / painting

You can **paint** compounds with colours that can be renamed, i.e. “Yes”, “No”, “Maybe”:

<img src="_static/media/rhs_colours.png" alt="lhs" width="400px">

These labels will be assigned to compounds in your session and can be downloaded as a CSV in the “selected compounds” tab

```{warning}
The state of the Fragalyis RHS does not persist when you refresh or otherwise leave the page. To export a copy of your curations remember to download a CSV:

<img src="_static/media/download_csv.png" alt="lhs" width="147px">
```

### Arrows

Use these arrows to quickly apply the current visualisations to adjacent compounds

This works best when inspirations modal is open, and the inspiration hits and current compound are shown as ligands

### Exporting curations

Once you have [painted](#colours-painting) compounds you can export a CSV which can be used to share your curations/review with others:

<img src="_static/media/download_csv.png" alt="lhs" width="147px">

Compounds from different sets they can be viewed together in the “selected compounds” tab.

---

(uploading-virtual)=
## Uploading virtual compound sets (RHS)

In order to disseminate non-experimental structures/ligands with Fragalysis, they can be uploaded using the "RHS upload" option in the "Hamburger menu", which takes you to the `viewer/upload_cset` endpoint:

<img src="_static/media/upload_cset.png" alt="lhs" width="400px">

### Supported data format

To upload a compound set to the RHS of Fragalysis an SD file (SDF) must be prepared. 

### Header molecule

Fragalysis requires a **header** molecule that defines properties for the whole compound set. The molecule and coordinates of the header molecule are completely ignored, however there are required properties:


|        Property         |                     Value                     |
|-------------------------|-----------------------------------------------|
| `_Name`                 | `ver_1.2`                                     |
| `ref_url`               | Reference URL for the algorithm / dataset     |
| `submitter_name`        | Compound set submitter's name                 |
| `submitter_email`       | Compound set submitter's email                |
| `submitter_institution` | Compound set submitter's institution          |
| `generation_date`       | Date associated with the data (ISO 8601)      |
| `method`                | Algorithm / method name for this compound set |


Additionally, if you want to include extra text or numerical properties for ligands in this set you will have to include that property in the header as well with a description value. For example if you want to include a `energy_score` property with each ligand you will need to include this as a property on the header as well, with a text description:

|        Property         |                     Value                     |
|-------------------------|-----------------------------------------------|
| `energy_score`                 | `Computed binding energy (kcal/mol)`|

An example header molecule is provided [below](#example-header).

### Ligands

The required properties for each **non-header** molecule are different:


|  Property  |                                                Value                                                 |
|------------|------------------------------------------------------------------------------------------------------|
| `_Name`    | compound name                                                                                        |
| `ref_pdb`  | Reference protein (Fragalysis observation short-code, e.g. A0310a)                                   |
| `ref_mols` | Reference datasets that inspired this molecule/pose (Fragalysis observation short-code, e.g. A0310a) |

### Ligands and proteins (SDF + ZIP of PDBs)

If you have computed custom protein conformations associated with these ligands they can be provided in the upload form as a separate ZIP archive. In this case, your `ref_pdb` values for each ligand should be the name of the relevant PDB file.

(example-header)=
### Example Header

```
ver_1.2
     RDKit          3D

 14 15  0  0  0  0  0  0  0  0999 V2000
   -3.4503    1.0190   -1.1743 C   0  0  0  0  0  0  0  0  0  0  0  0
   -2.2533    1.0671   -0.5344 N   0  0  0  0  0  0  0  0  0  0  0  0
   -2.1679   -0.0620    0.1865 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.3036   -0.8455    1.1366 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.4390   -1.7388    0.2452 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.3763   -0.9521   -0.6603 N   0  0  0  0  0  0  0  0  0  0  0  0
    1.4334   -0.1564   -0.1409 C   0  0  0  0  0  0  0  0  0  0  0  0
    2.0843   -0.7615    0.8099 N   0  0  0  0  0  0  0  0  0  0  0  0
    3.2028   -0.1250    1.4766 C   0  0  0  0  0  0  0  0  0  0  0  0
    4.1795    0.3255    0.4069 C   0  0  0  0  0  0  0  0  0  0  0  0
    3.7544    1.5811   -0.2821 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.9712    1.4810   -0.5890 S   0  0  0  0  0  0  0  0  0  0  0  0
   -3.3092   -0.7524   -0.0399 N   0  0  0  0  0  0  0  0  0  0  0  0
   -4.0785   -0.0801   -0.8706 O   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0
  2  3  1  0
  3  4  1  0
  4  5  1  0
  5  6  1  0
  6  7  1  0
  7  8  2  0
  8  9  1  0
  9 10  1  0
 10 11  1  0
 11 12  1  0
  3 13  2  0
 13 14  1  0
 14  1  1  0
 12  7  1  0
M  END
>  <ref_url>  (1) 
https://github.com/mwinokan/BulkDock

>  <submitter_name>  (1) 
Max Winokan

>  <submitter_email>  (1) 
max.winokan@diamond.ac.uk

>  <submitter_institution>  (1) 
DLS

>  <generation_date>  (1) 
2024-12-02

>  <method>  (1) 
Knitwork_CavB_impure

>  <SLURM_JOB_ID>  (1) 
SLURM_JOB_ID

>  <SLURM_JOB_NAME>  (1) 
SLURM_JOB_NAME

>  <csv_name>  (1) 
csv_name

>  <scratch_subdir>  (1) 
scratch_subdir

>  <fragmenstein_runtime>  (1) 
fragmenstein_runtime

>  <fragmenstein_outcome>  (1) 
fragmenstein_outcome

>  <fragmenstein_mode>  (1) 
fragmenstein_mode

>  <fragmenstein_error>  (1) 
fragmenstein_error

>  <exports>  (1) 
exports

>  <HIPPO Pose ID>  (1) 
HIPPO Pose ID

>  <HIPPO Compound ID>  (1) 
HIPPO Compound ID

>  <smiles>  (1) 
smiles

>  <ref_pdb>  (1) 
protein reference

>  <ref_mols>  (1) 
fragment inspirations

>  <original ID>  (1) 
original ID

>  <compound inchikey>  (1) 
compound inchikey
```