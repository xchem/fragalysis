from urllib.parse import urljoin
from .session import _session
from .urls import COMPOUNDS_URL, TARGETS_URL, SITE_OBSERVATIONS_URL
import mrich


def get_target_compound_smiles(
    stack: str = "production", token: str | None = None
) -> dict[str, set[str]]:
    """
    Use the /api/target_molecules/ endpoint to get the SMILES of all compounds associated with each target in the legacy stack.

    :param stack: The stack to query. Defaults to "production".
    :param token: Optional authentication token for the API request. If None, uses default session authentication. Defaults to None.
    :return: A dictionary mapping target names to sets of associated compound SMILES.
    :rtype: dict[str, set[str]]
    """

    with _session(stack=stack, token=token) as session:

        match stack:
            case "legacy":

                response = session.get(urljoin(session.root, "/api/target_molecules/"))

                if not response.ok:
                    raise Exception(
                        f"Failed to get target compounds: {response.status_code} - {response.text}"
                    )

                data = response.json()

                smiles_by_target = {}

                for target_data in data["results"]:

                    target_name = target_data["title"]
                    smiles_by_target.setdefault(target_name, set())

                    for molecule_data in target_data["molecules"]:
                        smiles_by_target[target_name].add(
                            molecule_data["data"]["smiles"]
                        )

                return smiles_by_target

            case _:

                # assuming v2 stack

                from .download import target_list

                # targets
                targets_url = urljoin(session.root, TARGETS_URL)
                mrich.debug(f"GET {targets_url}")
                target_response = session.get(targets_url)

                if not target_response.ok:
                    raise Exception(
                        "Request failed", targets_url, target_response.status_code
                    )

                targets_data = target_response.json()

                targets = {t["id"]: t["title"] for t in targets_data["results"]}

                smiles_by_target = {}

                for target_id, target_title in targets.items():
                    mrich.var(target_title, target_id)

                    smiles_by_target.setdefault(target_title, set())

                    observations_url = urljoin(session.root, SITE_OBSERVATIONS_URL)
                    mrich.debug(f"GET {observations_url}")
                    response = session.get(
                        observations_url, params={"target": target_id}
                    )

                    if not response.ok:
                        raise Exception(
                            "Request failed", observations_url, response.status_code
                        )

                    data = response.json()

                    for observation in data["results"]:
                        smiles = observation["smiles"]
                        smiles_by_target[target_title].add(smiles)

                return smiles_by_target
