
# Creating direct URLs to specific views

To link to specific datasets within a target, the following syntax is supported:

## Specifying the target and proposal

The following URL takes you to the target with:

- name: `A71EV2A`
- target access string (tas): `lb32627-66`:

[https://fragalysis.diamond.ac.uk/viewer/react/preview/target/A71EV2A/tas/lb32627-66](https://fragalysis.diamond.ac.uk/viewer/react/preview/target/A71EV2A/tas/lb32627-66)


## Using the `direct` URL syntax

You can also create URLs that display specific datasets. To use this functionality you have to use this base URL including the `direct` command:

```
https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/
```

### e.g. showing observations with ligands where compound alias contains substring `ASAP`:

[https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP/L](https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP/L)

- `target/A71EV2A`: specifies the target name
- `tas/lb32627-66`: specifies the target access string
- `compound/ASAP/L`: shows the ligand (`L`) representation for all `compound` aliases containing `ASAP`

### e.g. showing observations with ligands where compound alias is exactly `ASAP-0016733-001`:

[https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP-0016733-001/L/exact](https://fragalysis.diamond.ac.uk/viewer/react/preview/direct/target/A71EV2A/tas/lb32627-66/compound/ASAP-0016733-001/L/exact)

- `target/A71EV2A`: specifies the target name
- `tas/lb32627-66`: specifies the target access string
- `compound/ASAP-0016733-001/L/exact`: shows the ligand (`L`) representation for exact `compound` aliases match `ASAP-0016733-001`

