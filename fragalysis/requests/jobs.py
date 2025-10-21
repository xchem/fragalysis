import mrich
from mrich import print

import time
import pandas as pd
from json import JSONDecodeError, dumps
from urllib.parse import urljoin, quote, unquote

from .session import _session
from .urls import (
    SESSION_PROJECTS_URL,
    SNAPSHOTS_URL,
    JOB_REQUEST_URL,
    JOB_TRANSFER_URL,
    SITE_OBSERVATIONS_URL,
    TASK_STATUS_URL,
    USER_URL,
)

"""

0. Ensure job over-rides exist on stack (/api/job_override)
1. Create session project (/api/session-projects/)
2. Create snapshot (/api/snapshots/)
3. Transfer snapshot (/api/job_file_transfer/)

"""


def fragmenstein_placement(
    placements: list[dict],
    target_name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
):
    """Pass a list of dictionaries with placement tasks:

    [{
        "smiles": ...,
        "inspirations": ["A0310a", "A0226a"],
        "protein": "A0310a",
    }]

    """

    from .download import target_list

    mrich.var("target_name", target_name)
    mrich.var("tas", tas)
    mrich.var("stack", stack)
    mrich.var("#placements", len(placements))

    author_id = user_info(stack=stack, token=token)["user_id"]

    if author_id == 1:
        mrich.error("Unauthenticated user, is token valid?")
        return None

    mrich.var("user_id", author_id)

    # GET TARGET AND PROJECT INFO

    targets, projects = target_list(stack=stack, token=token, return_project_data=True)

    for target_id, name, proposal in targets:
        if name == target_name and proposal == tas:
            break
    else:
        mrich.error("Target not found", target_name, tas)
        return None

    mrich.var("target_id", target_id)

    for project_id, proposal in projects.items():
        if proposal == tas:
            break

    mrich.var("project_id", project_id)

    # GET SITE OBSERVATIONS

    with mrich.loading("Getting site observations..."):
        site_observations_data = site_observations(
            token=token,
            stack=stack,
            target_id=target_id,
        )

    site_observations_df = pd.DataFrame(site_observations_data)
    site_observations_df = site_observations_df.set_index("code")

    # GROUP TASKS BASED ON PROTEIN AND INSPIRATIONS

    tasks = {}

    with mrich.loading("Grouping placements..."):
        for d in placements:
            smiles = str(d["smiles"])
            inspirations = [str(i) for i in d["inspirations"]]
            protein = str(d["protein"])

            task_key = (protein, tuple(sorted(inspirations)))
            tasks.setdefault(task_key, [])
            tasks[task_key].append(smiles)

    mrich.var("#jobs", len(tasks))

    ### START ALL THE FILE TRANSFERS

    transfer_tasks = []

    with mrich.loading("Requesting file transfers..."):
        for (reference, inspirations), smiles_strs in tasks.items():

            # GET FILENAMES

            reference_file = site_observations_df.loc[reference, "apo_desolv_file"]
            reference_file = clean_filepath(reference_file)

            inspiration_files = set()
            for inspiration in inspirations:
                file = site_observations_df.loc[inspiration, "ligand_mol"]
                file = clean_filepath(file)
                inspiration_files.add(file)

            # CREATE SESSION PROJECT

            session_project_dict = create_session_project(
                token=token,
                author_id=author_id,
                target_id=target_id,
                project_id=project_id,
                stack=stack,
            )

            # CREATE SNAPSHOT

            snapshot_dict = create_snapshot(
                token=token,
                author_id=author_id,
                stack=stack,
                session_project_id=session_project_dict["id"],
            )

            # CREATE FILE TRANSFER

            transfer_dict = transfer_snapshot(
                token=token,
                snapshot_id=snapshot_dict["id"],
                session_project_id=session_project_dict["id"],
                target_id=target_id,
                stack=stack,
                protein_files=[reference_file],
                compound_files=inspiration_files,
            )

            if not transfer_dict:
                return None

            transfer_dict["session_project"] = session_project_dict
            transfer_dict["snapshot"] = snapshot_dict
            transfer_dict["reference"] = reference
            transfer_dict["inspirations"] = inspirations
            transfer_dict["smiles_strs"] = smiles_strs
            transfer_dict["reference_file"] = reference_file
            transfer_dict["inspiration_files"] = inspiration_files

            transfer_tasks.append(transfer_dict)

    # MONITOR TASK

    completed = set()

    with mrich.clock("Waiting for file transfers to complete..."):
        with _session(stack=stack, token=token) as session:
            for i in range(100_000):

                if len(completed) == len(transfer_tasks):
                    break

                for task in transfer_tasks:

                    task_id = task["transfer_task_id"]

                    if task_id in completed:
                        continue

                    status_url = urljoin(session.root, TASK_STATUS_URL + task_id)

                    status = session.get(status_url)

                    try:
                        status_json = status.json()
                    except JSONDecodeError:
                        continue

                    finished = "SUCCESS" in status.text

                    if finished:
                        mrich.success("Job transfer complete", task_id)
                        completed.add(task_id)

                time.sleep(0.5)

            else:
                mrich.error("Timed out")
                raise ValueError

    ### START ALL THE PLACEMENT JOBS

    """Use fragmenstein-place-file job: 
    
    https://github.com/InformaticsMatters/squonk2-fragmenstein/blob/00e7ee93f659b80f175577d534cb5420b23f7dce/data-manager/fragmenstein.yaml#L180

    - fragments (inspirations)
    - protein (reference)
    - smiles (list of smiles strings)

    job-spec must be valid JSON:

    "squonk_job_spec": "{
        "collection":"fragmenstein",
        "job":"fragmenstein-combine",
        "version":"1.0.0",
        "variables":{
            "fragments":[
                    "fragalysis-files/irnh/5r7y_A_1001_1_7gbd%2BA%2B404%2B1_ligand.mol",
                    "fragalysis-files/irnh/5r7z_A_404_1_7gbd%2BA%2B404%2B1_ligand.mol"
                ],
            "count":5,
            "fragIdField":"_Name",
            "keepHydrogens":false,
            "outfile":"fragalysis-jobs/spf57946/fragmenstein-combine-1750410737796/merged.sdf",
            "proteinFieldName":"ref_pdb",
            "proteinFieldValue":"5r7z_A_404_1_7gbd%2BA%2B404%2B1_apo-desolv.pdb",
            "smilesFieldName":"original SMILES",
            "protein":"fragalysis-files/irnh/5r7z_A_404_1_7gbd%2BA%2B404%2B1_apo-desolv.pdb"
        }
    }"
    
    """

    placement_tasks = []

    with mrich.loading("Starting placement jobs..."):
        for i, transfer_dict in enumerate(transfer_tasks):

            job_spec = dict(
                collection="fragmenstein",
                job="fragmenstein-place-string",
                version="1.0.0",
                variables=dict(
                    protein=transfer_dict["reference_file"],
                    fragments=list(transfer_dict["inspiration_files"]),
                    smiles=list(transfer_dict["smiles_strs"]),
                ),
            )

            payload = dict(
                access=project_id,
                target=target_id,
                snapshot=transfer_dict["snapshot"]["id"],
                session_project=transfer_dict["session_project"]["id"],
                squonk_job_name=f"placement-{i+1}",
                squonk_job_spec=dumps(job_spec),
            )

            with _session(stack=stack, token=token) as session:

                url = urljoin(session.root, JOB_REQUEST_URL)

                print(payload)

                response = session.post(url, data=payload)

                if not response.ok:
                    mrich.error("Request failed", url, response.status_code)
                    mrich.print(response.text)
                return None

            json = response.json()

            print(json)

    # MONITOR JOB


def user_info(
    stack: str = "production",
    token: str | None = None,
) -> dict:

    with _session(stack, token) as session:

        url = urljoin(session.root, USER_URL)

        response = session.post(url)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            return None

        try:
            json = response.json()
        except JSONDecodeError:
            mrich.error("Can't get user info, is token valid?")
            return None

        return json


def site_observations(
    target_id: int | None = None,
    stack: str = "production",
    token: str | None = None,
) -> dict:

    with _session(stack, token) as session:

        url = urljoin(session.root, SITE_OBSERVATIONS_URL)

        if target_id:
            response = session.post(url, params=dict(target=target_id))
        else:
            response = session.post(url)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            return None

        json = response.json()

        return json["results"]


def transfer_snapshot(
    token: str,
    snapshot_id: int,
    session_project_id: int,
    target_id: int,
    protein_files: list[str],
    compound_files: list[str],
    stack: str = "production",
):

    proteins = ",".join(protein_files)
    compounds = ",".join(compound_files)

    payload = dict(
        snapshot=snapshot_id,
        session_project=session_project_id,
        access=2,
        target=target_id,
        proteins=proteins,
        compounds=compounds,
    )

    with _session(stack, token) as session:

        url = urljoin(session.root, JOB_TRANSFER_URL)
        response = session.post(url, data=payload)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            if response.status_code == 403:
                mrich.error("Is token valid?")
            return None

        json = response.json()

        return json


def create_session_project(
    token: str,
    author_id: int,
    target_id: int,
    project_id: int,
    *,
    stack: str = "production",
    title: str = "API created project",
    description: str = "API created project",
) -> dict:

    tags = []

    with _session(stack, token) as session:

        payload = dict(
            author=author_id,
            target=target_id,
            project=project_id,
            title=title,
            description=description,
            tags=tags,
        )

        # mrich.print(payload)

        sp_url = urljoin(session.root, SESSION_PROJECTS_URL)
        response = session.post(sp_url, data=payload)

        if not response.ok:
            mrich.error("Request failed", sp_url, response.status_code)
            mrich.print(response.text)
            return None

        sp = response.json()

        return sp


def create_snapshot(
    token: str,
    author_id: int,
    session_project_id: int,
    *,
    stack="production",
    title: str = "API created snapshot",
    description: str = "API created snapshot",
):

    payload = dict(
        author=author_id,
        session_project=session_project_id,
        title=title,
        description=description,
        type="INIT",
        data="[]",
        parent=None,
        children=[],
        additional_info=None,
    )

    with _session(stack, token) as session:

        url = urljoin(session.root, SNAPSHOTS_URL)
        response = session.post(url, data=payload)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            return None

        snapshot = response.json()

        return snapshot


def get_last_session_project_id(
    target_id: int,
    author_id: int,
    # project: str,
    stack: str = "production",
):

    with _session(stack) as session:

        sp_url = urljoin(session.root, SESSION_PROJECTS_URL)
        response = session.get(sp_url, params=dict(target=target_id, author=author_id))

        if not response.ok:
            mrich.error("Request failed", sp_url, response.status_code)
            return None

        sps = response.json()

    df = pd.DataFrame(sps["results"])
    return df.sort_values(by="init_date").iloc[-1]["id"]


def clean_filepath(path):
    path = unquote(path)
    return path.split("/media/")[-1]
