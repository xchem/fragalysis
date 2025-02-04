
# Browsing Experimental (LHS) data

The left-hand-side (LHS) user interface of Fragalysis allows you to select experimental data for display, download, and computation.

There are two panels:

- [Tag Details](#tag-details)
- [Hit navigator](#hit-navigator)

<img src="_static/media/lhs_ui.png" alt="lhs" width="600px">

## Tag Details

<img src="_static/media/lhs_tag_panel.png" alt="lhs" width="600px">

All tags assigned to left-hand side data can be managed in this panel.

This section details how tags can be used to filter experimental data. To add and edit tags see the [Tagging/curating experimental (LHS) data](tags) page.

### Selecting tag(s)

Select tags to show datasets assigned to that tag in the [Hit navigator](#hit-navigator). The union / intersection toggle at the top of the page can be used to determine the behaviour when multiple tags are selected:

- **Union**: Display datasets that are tagged with **at least one** of the selected tags
- **Intersection**: Display datasets that are tagged with **all** of the selected tags

### Show all hits

The **SHOW ALL HITS** button overrides the tag selection and shows datasets regardless of tag

### Select all tags

The **SELECT ALL TAGS** button selects all tags

### Select hits belonging to a tag

To select (activate checkboxes) in the hit navigator for all datasets belonging to a specific tag use the **SELECT HITS** buttons next to each tag.

## Hit navigator

<img src="_static/media/lhs_hit_panel.png" alt="lhs" width="600px">

### LHS "poses" and "observations"

Ligands from experimental datasets are known as **observations** are grouped into **poses**. **Poses** are named after and take their behaviour from their **main observation**. 

**Poses** and **observations** have the following interface:

<img src="_static/media/lhs_pose.pdf" alt="lhs" width="600px">

### What decides which hits are shown?

The hit navigator follows these key rules to determine which datasets are shown:

1. All datasets displayed in the 3d viewer are shown
1. Datasets from active tags are shown
1. If a search string is present, only observations matching that string are shown
