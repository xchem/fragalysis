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


def knitwork(
    observations: list[str],
    target_name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
):
    """Run Knitwork pure and impure merging on provided observation names"""

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
            compound_files=ligand_files,
        )

        if not transfer_dict:
            return None

        transfer_dict["session_project"] = session_project_dict
        transfer_dict["snapshot"] = snapshot_dict
        transfer_dict["observations"] = observations
        transfer_dict["ligand_files"] = ligand_files

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

    ### START THE KNITWORK JOB

    with mrich.loading("Starting knitwork job..."):

        project_directory = transfer_dict["transfer_root"]
        mrich.var("project_directory", project_directory)

        job_spec = dict(
            collection="knitwork",
            job="knitwork",
            version="1.0.0",
        )

        payload = dict(
            access=project_id,
            target=target_id,
            snapshot=transfer_dict["snapshot"]["id"],
            session_project=transfer_dict["session_project"]["id"],
            squonk_job_name=f"placement-{i+1}",
            squonk_job_spec=dumps(job_spec),
            variables=dict(
                ligands=[
                    modify_filepath(p, project_directory)
                    for p in transfer_dict["ligand_files"]
                ],
            ),
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

    # MONITOR JOB

    return urljoin(DATA_MANAGERS[stack], json["squonk_url_ext"])

    # GET OUTPUTS
