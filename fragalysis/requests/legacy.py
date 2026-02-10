
from urllib.parse import urljoin
from .session import _session

def get_target_compound_smiles() -> dict[str, set[str]]:
    """
    Use the /api/target_molecules/ endpoint to get the SMILES of all compounds associated with each target in the legacy stack.
    
    :return: A dictionary mapping target names to sets of associated compound SMILES.
    :rtype: dict[str, set[str]]
    """

    with _session(stack="legacy", token=None) as session:

        response = session.get(urljoin(session.root, "/api/target_molecules/"))

        if not response.ok:
            raise Exception(f"Failed to get target compounds: {response.status_code} - {response.text}")
        
        data = response.json()

        smiles_by_target = {}

        for target_data in data["results"]:

            target_name = target_data["title"]
            smiles_by_target.setdefault(target_name, set())

            for molecule_data in target_data["molecules"]:
                smiles_by_target[target_name].add(molecule_data["data"]["smiles"])

        return smiles_by_target
