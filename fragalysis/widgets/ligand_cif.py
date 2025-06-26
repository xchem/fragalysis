import mrich
from pathlib import Path
import ipywidgets

import molparse as mp
from rdkit import Chem
from rdkit.Chem import AllChem
import gemmi


def ligand_cif():
    """UI for downloading targets from fragalysis"""
    _cif_ui_1()


def _cif_ui_1():
    """Create widgets to create a ligand CIF file"""

    mrich.h3("ligand CIF")

    w_dir = ipywidgets.Text(description="Directory", value=".")

    ui_1 = ipywidgets.VBox()
    ui_main = ipywidgets.VBox([ui_1])

    output = ipywidgets.Output()

    b_get_pdbs = ipywidgets.Button(
        description="Get PDB list",
    )

    def button_func(button):
        with output:
            _cif_ui_2(ui_main=ui_main, dir=w_dir.value)

    b_get_pdbs.on_click(button_func)

    ui_1.children = [w_dir, b_get_pdbs, output]

    display(ui_main)


def _cif_ui_2(ui_main, dir: str = "."):
    """widgets to request target download"""

    output = ipywidgets.Output()

    ui_2 = ipywidgets.VBox()

    pdbs = sorted([p.name for p in Path(dir).glob("*.pdb")])

    if not pdbs:
        with output:
            mrich.error("No PDB files in this directory.")
            ui_main.children = [ui_main.children[0], output]
            return

    w_pdb = ipywidgets.Dropdown(
        options=pdbs,
        description="PDB File",
    )

    b_download = ipywidgets.Button(
        description="Parse PDB",
    )

    def button_func(button):
        with output:
            _cif_ui_3(ui_main=ui_main, pdb=Path(dir) / w_pdb.value)

    b_download.on_click(button_func)

    ui_2.children = [w_pdb, b_download, output]
    ui_main.children = [ui_main.children[0], ui_2]


def _cif_ui_3(ui_main, pdb: Path):

    output = ipywidgets.Output()

    with output:
        sys = mp.parse(pdb, verbosity=0)

    ui_3 = ipywidgets.VBox()

    ligs = [r for r in sys.residues if r.type == "LIG"]
    options = [r.name_number_chain_str for r in ligs]

    w_lig = ipywidgets.Dropdown(
        options=options,
        description="Residue",
    )

    w_smiles = ipywidgets.Text(description="SMILES", value=None)

    cif = pdb.parent / f'{pdb.name.removesuffix(".pdb")}.cif'
    w_cif = ipywidgets.Text(description="Output", value=str(cif))

    b_create = ipywidgets.Button(
        description="Create CIF",
    )

    def button_func(button):
        with output:

            res = ligs[options.index(w_lig.value)]

            create_cif(cif=Path(w_cif.value), smiles=w_smiles.value, res=res)

    b_create.on_click(button_func)

    ui_3.children = [w_lig, w_smiles, w_cif, b_create, output]
    ui_main.children = [ui_main.children[0], ui_main.children[1], ui_3]


def create_cif(cif: Path, smiles: str, res):

    mol = res.rdkit_mol
    conf = mol.GetConformer()
    refmol = mp.rdkit.mol_from_smiles(smiles)
    mol = AllChem.AssignBondOrdersFromTemplate(refmol, mol)
    Chem.Kekulize(mol, clearAromaticFlags=True)

    # Create CIF document
    doc = gemmi.cif.Document()
    block = doc.add_new_block("LIG")

    # Step 3: Atom loop (_chem_comp_atom)
    atom_loop = block.init_loop(
        "_chem_comp_atom.", ["comp_id", "atom_id", "type_symbol", "x", "y", "z"]
    )

    for i, atom in enumerate(mol.GetAtoms()):
        pos = conf.GetAtomPosition(i)
        atom_id = f"{atom.GetSymbol()}{i}"
        atom_loop.add_row(
            [
                "LIG",
                atom_id,
                atom.GetSymbol(),
                f"{pos.x:.3f}",
                f"{pos.y:.3f}",
                f"{pos.z:.3f}",
            ]
        )

    # Step 4: Bond loop (_chem_comp_bond)
    bond_loop = block.init_loop(
        "_chem_comp_bond.", ["comp_id", "atom_id_1", "atom_id_2", "value_order"]
    )

    bond_order_map = {1: "single", 2: "double", 3: "triple", 1.5: "aromatic"}

    for bond in mol.GetBonds():
        idx1 = bond.GetBeginAtomIdx()
        idx2 = bond.GetEndAtomIdx()
        order = bond.GetBondTypeAsDouble()
        bond_loop.add_row(
            [
                "LIG",
                f"{mol.GetAtomWithIdx(idx1).GetSymbol()}{idx1}",
                f"{mol.GetAtomWithIdx(idx2).GetSymbol()}{idx2}",
                bond_order_map.get(order, "single"),
            ]
        )

    # Step 5: Write CIF to file
    with open(cif, "w") as f:
        mrich.writing(cif)
        f.write(doc.as_string())
