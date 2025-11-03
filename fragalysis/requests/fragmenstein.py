import mrich

import time
import pandas as pd
from urllib.parse import urljoin
from json import JSONDecodeError, dumps

from .common import user_info, site_observations
from .session import _session
from .urls import TASK_STATUS_URL, JOB_REQUEST_URL
from .squonk import DATA_MANAGERS, SQUONK_DM_INSTANCE_URL

from .jobs import (
    clean_filepath,
    modify_filepath,
    create_session_project,
    create_snapshot,
    transfer_snapshot,
)


def fragmenstein_place(
    placements: list[dict],
    target_name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
    num_repeats: int = 1,
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
    mrich.var("#repeats", num_repeats)

    author_dict = user_info(stack=stack, token=token)
    author_id = author_dict["user_id"]

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

    # MONITOR FILE TRANSFER TASKS

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

    with mrich.loading("Starting placement jobs..."):
        for i, transfer_dict in enumerate(transfer_tasks):

            project_directory = transfer_dict["transfer_root"]
            mrich.var("project_directory", project_directory)

            output_file = f"{project_directory}/placed.sdf"
            mrich.var("output_file", output_file)

            job_spec = dict(
                collection="fragmenstein",
                job="fragmenstein-place-string",
                version="1.0.0",
                variables=dict(
                    protein=modify_filepath(
                        transfer_dict["reference_file"],
                        project_directory,
                    ),
                    fragments=[
                        modify_filepath(p, project_directory)
                        for p in transfer_dict["inspiration_files"]
                    ],
                    smiles=list(transfer_dict["smiles_strs"]),
                    outfile=output_file,
                    count=num_repeats,
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

                response = session.post(url, data=payload)

                if not response.ok:
                    mrich.error("Request failed", url, response.status_code)
                    mrich.print(response.text)
                    return None

                json = response.json()

                transfer_dict["squonk_url_ext"] = json["squonk_url_ext"]
                transfer_dict["job_request_id"] = json["id"]
                transfer_dict["squonk_instance"] = json["squonk_url_ext"].split(
                    "instance/"
                )[-1]

                mrich.success(
                    "Job request submitted", json["id"], json["squonk_url_ext"]
                )

    # MONITOR JOB

    completed = set()

    with mrich.clock("Waiting for placement jobs to complete..."):
        with _session(stack=stack, token=token) as session:
            for i in range(100_000):

                if len(completed) == len(transfer_tasks):
                    break

                for task in transfer_tasks:

                    instance = task["squonk_instance"]

                    if instance in completed:
                        continue

                    status_url = urljoin(
                        DATA_MANAGERS[stack], SQUONK_DM_INSTANCE_URL + instance
                    )

                    status = session.get(status_url)

                    try:
                        status_json = status.json()
                    except JSONDecodeError:
                        continue

                    squonk_task_ids = [d["id"] for d in status_json["tasks"]]

                    if len(squonk_task_ids) != 0:
                        raise ValueError("Wrong number of squonk tasks")

                    task["squonk_task"] = squonk_task_ids[0]

                    status_url = urljoin(
                        DATA_MANAGERS[stack], SQUONK_DM_TASK_URL + task["squonk_task"]
                    )

                    status = session.get(status_url)

                    try:
                        status_json = status.json()
                    except JSONDecodeError:
                        continue

                    finished = status["done"]

                    if finished:
                        mrich.success("Placement job complete", instance)
                        completed.add(instance)

                time.sleep(0.5)

            else:
                mrich.error("Timed out")
                raise ValueError


def fragmenstein_combine(
    observations: list[str],
    protein: str,
    target_name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
    num_repeats: int = 1,
    multi: bool = True,
    min_combine: int = 2,
    max_combine: int = 3,
    max_distance: float = 1.5,
):
    """Run Fragmenstein combine on provided observation names, or subset pairs/triples if multi is selected."""

    from .download import target_list

    mrich.var("target_name", target_name)
    mrich.var("tas", tas)
    mrich.var("stack", stack)
    mrich.var("#observations", len(observations))

    author_dict = user_info(stack=stack, token=token)
    author_id = author_dict["user_id"]

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

    ### START THE FILE TRANSFER

    with mrich.loading("Requesting file transfer..."):

        ligand_files = set()

        for observation in observations:
            file = site_observations_df.loc[observation, "ligand_mol"]
            file = clean_filepath(file)
            ligand_files.add(file)

        file = site_observations_df.loc[protein, "apo_desolv_file"]
        file = clean_filepath(file)
        protein_files = [file]

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
            protein_files=protein_files,
            compound_files=ligand_files,
        )

        if not transfer_dict:
            return None

        transfer_dict["session_project"] = session_project_dict
        transfer_dict["snapshot"] = snapshot_dict
        transfer_dict["observations"] = observations
        transfer_dict["ligand_files"] = ligand_files
        transfer_dict["protein_files"] = protein_files

    # MONITOR FILE TRANSFER

    with mrich.clock("Waiting for file transfer to complete..."):
        with _session(stack=stack, token=token) as session:
            for i in range(100_000):

                task_id = transfer_dict["transfer_task_id"]

                status_url = urljoin(session.root, TASK_STATUS_URL + task_id)

                status = session.get(status_url)

                try:
                    status_json = status.json()
                except JSONDecodeError:
                    continue

                finished = "SUCCESS" in status.text

                if finished:
                    mrich.success("Job transfer complete", task_id)
                    break

                time.sleep(0.5)

            else:
                mrich.error("Timed out")
                raise ValueError

    ### START THE FRAGMENSTEIN JOB

    with mrich.loading("Starting fragmenstein job..."):

        project_directory = transfer_dict["transfer_root"]
        mrich.var("project_directory", project_directory)

        output_file = f"{project_directory}/merged.sdf"
        mrich.var("output_file", output_file)

        job_spec = dict(
            collection="fragmenstein",
            version="1.0.0",
            variables=dict(
                protein=modify_filepath(
                    transfer_dict["protein_files"][0],
                    project_directory,
                ),
                fragments=[
                    modify_filepath(p, project_directory)
                    for p in transfer_dict["ligand_files"]
                ],
                outfile=output_file,
                count=num_repeats,
            ),
        )

        if multi:
            job_spec["job"] = "fragmenstein-combine-multi"
            job_spec["variables"]["minNum"] = min_combine
            job_spec["variables"]["maxNum"] = max_combine
            job_spec["variables"]["maxDist"] = max_distance
        else:
            job_spec["job"] = "fragmenstein-combine"

        payload = dict(
            access=project_id,
            target=target_id,
            snapshot=transfer_dict["snapshot"]["id"],
            session_project=transfer_dict["session_project"]["id"],
            squonk_job_name=f"{target_name} fragmenstein-merge",  # this does not end up in squonk...
            squonk_job_spec=dumps(job_spec),
        )

        with _session(stack=stack, token=token) as session:

            url = urljoin(session.root, JOB_REQUEST_URL)

            response = session.post(url, data=payload)

            if not response.ok:
                mrich.error("Request failed", url, response.status_code)
                mrich.print(response.text)
                return None

            json = response.json()

            transfer_dict["squonk_url_ext"] = json["squonk_url_ext"]
            transfer_dict["job_request_id"] = json["id"]
            transfer_dict["squonk_instance"] = json["squonk_url_ext"].split(
                "instance/"
            )[-1]

            mrich.success("Job request submitted", transfer_dict["squonk_instance"])

            mrich.var("instance_id", transfer_dict["squonk_instance"])

    return urljoin(DATA_MANAGERS[stack], json["squonk_url_ext"])
