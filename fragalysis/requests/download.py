import datetime
import random
import re
import time
import mrich

from pathlib import Path
from json import JSONDecodeError
from urllib.parse import urljoin

from .session import _session, debug_requests_on
from .urls import PROJECTS_URL, TARGETS_URL, DOWNLOAD_URL, TARGET_EXPERIMENT_UPLOADS_URL, RE_DOWNLOAD_TARGET_FILENAME

# Seed the random number generator
random.seed()

_DOWNLOAD_MIN_SLEEP: int = 2
_DOWNLOAD_MAX_SLEEP: int = 12

def target_list(
    stack: str = "production",
    token: str | None = None,
    return_project_data: bool = False,
) -> list[dict]:
    """Request a list of target dictionaries from a Fragalysis deployment

    :param stack: shorthand or URL of Fragalysis deployment, defaults to "production"
    :param token: optional authentication token
    :returns: list of target dictionaries with "id", "title", and "project" keys
    """

    with _session(stack, token) as session:

        # projects
        projects_url = urljoin(session.root, PROJECTS_URL)
        project_response = session.get(projects_url)

        if not project_response.ok:
            mrich.error("Request failed", projects_url, project_response.status_code)
            return None

        # targets
        targets_url = urljoin(session.root, TARGETS_URL)
        target_response = session.get(targets_url)

        if not target_response.ok:
            mrich.error("Request failed", targets_url, target_response.status_code)
            return None

        targets_data = target_response.json()
        projects_data = project_response.json()

        projects = {
            d["id"]: d["target_access_string"] for d in projects_data["results"]
        }

        targets = []
        for d in targets_data["results"]:
            targets.append((d["id"], d["title"], projects[d["project"]]))

        if return_project_data:
            return targets, projects

        return targets


def download_target(
    name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
    destination: str = ".",
    metadata_file: bool = True,
    combined_sdf: bool = True,
    compound_set_sdfs: bool = True,
    soakdb_files: bool = True,
    unaligned_pdbs: bool = False,
    ligand_cifs: bool = False,
    event_maps: bool = False,
    inspection_maps: bool = False,
    residual_maps: bool = False,
    real_space_maps: bool = False,
    transformation_files: bool = False,
    reflections_files: bool = False,
    extract: bool = True,
    debug: bool = False,
    iteration: int = 1,
    debug_requests: bool = False
) -> None:
    """Request a target download from a Fragalysis deployment

    :param name: name of the target to request
    :param tas: target access string of the target
    :param stack: shorthand or URL of Fragalysis deployment, defaults to "production"
    :param token: optional authentication token
    :param destination: directory within which to place the download, defaults to "." (current working directory)
    :param metadata_file: Download metadata.csv?
    :param combined_sdf: Download single SDF of all ligands?
    :param compound_set_sdfs: Download RHS / computed ligand SDFs?
    :param soakdb_files: Download SoakDB CSV/sqlite files?
    :param unaligned_pdbs: Download coordinate files (not re-aligned) (.pdb)?
    :param ligand_cifs: Download ligand definitions and geometry restrains (.cif)?
    :param event_maps: Download PanDDA Event maps - primary evidence?
    :param inspection_maps: Download conventional inspection maps ("2FoFc")?
    :param residual_maps: Download conventional residual maps ("FoFc")?
    :param real_space_maps: Real-space map files (VERY BIG!) (.map)?
    :param transformation_files: Download transformations applied for alignments?
    :param reflections_files: Download reflections and map coefficients (.mtz)?
    :param extract: Extract the downloaded zip / tar archive?
    :param debug: Add print debug displaying the change in download status text
    :param iteration: A number used to distinguish output messages (important when downloading concurrent targets)
    :param debug_requests: True to set underlying HTTP request logging to DEBUG
    """

    payload = {
        "target_name": name,
        "target_access_string": tas,
        "all_aligned_structures": True,
        "cif_info": ligand_cifs,
        "diff_file": residual_maps,
        "event_file": event_maps,
        "map_info": real_space_maps,
        "metadata_info": metadata_file,
        "mtz_info": reflections_files,
        "pdb_info": unaligned_pdbs,
        "sigmaa_file": inspection_maps,
        "trans_matrix_info": transformation_files,
        "single_sdf_file": combined_sdf,
        "compound_sets": compound_set_sdfs,
        "file_url": "",
        "proteins": "",
        "static_link": False,
        "soakdb_files": soakdb_files,
    }

    destination = Path(destination)
    if not destination.exists():
        mrich.error(f"Download destination does not exist [{iteration}]: {destination}")
        return None

    if debug_requests:
        debug_requests_on()

    with _session(stack, token) as session:

        download_api_url = urljoin(session.root, DOWNLOAD_URL)

        with mrich.loading(f"Requesting download [{iteration}]"):

            start_download_process_response = session.post(
                download_api_url,
                data=payload,
            )

        if start_download_process_response.ok:
            response_json = start_download_process_response.json()
            # We might get a file_url or a task_status_url
            file_url = response_json.get("file_url")
            task_status_url = response_json.get("task_status_url")
            if not task_status_url and not file_url:
                mrich.error(f"No task or file URL returned [{iteration}] text={start_download_process_response.text}")
                raise ValueError("No task or file URL returned")

            # If given a task monitor it until we get a file link
            if task_status_url:
                # We continue checking the 'task' URL
                # until we find what looks like a download filename
                task_status_url = urljoin(session.root, task_status_url)
                file_url_re = re.compile(RE_DOWNLOAD_TARGET_FILENAME)
                last_status_text = ""
                last_message = ""
                file_url = ""
                with mrich.loading(f"Preparing download [{iteration}] (to '{destination}' task-url '{task_status_url}')"):
                    for _ in range(100_000):

                        status = session.get(task_status_url)
                        if debug and status.text != last_status_text:
                            last_status_text = status.text
                            now = datetime.datetime.now()
                            print(f"{now.strftime('%Y-%m-%d %H:%M')} [{iteration}] {status.text}")
                        if status.status_code != 200:
                            mrich.error(f"API did not respond with 200 [{iteration}]: {status.status_code} {status.text}")
                            mrich.error(f"Task Status URL [{iteration}]: '{task_status_url}'")
                            return

                        try:
                            status_json = status.json()
                        except JSONDecodeError:
                            continue

                        last_message = status_json.get("messages", "")
                        if last_message and file_url_re.match(last_message):
                            file_url = last_message
                            break

                        # Git it a rest - with a new random sleep period
                        time.sleep(random.randint(_DOWNLOAD_MIN_SLEEP, _DOWNLOAD_MAX_SLEEP))

                    else:
                        mrich.error(f"Download took too long [{iteration}]")
                        raise ValueError

            # If we get here we expect to have found a file-url in the API message
            if not file_url:
                mrich.error(f"Message does not name a tarball [{iteration}] message='{last_message}'")

            ### DOWNLOAD PREPARED PAYLOAD

            local_filename = destination / Path(file_url).name

            with mrich.loading(f"Downloading [{iteration}]..."):

                mrich.writing(f"[{iteration}] {local_filename}")

                with session.get(
                    download_api_url,
                    params=dict(file_url=file_url),
                    stream=True,
                ) as r:

                    r.raise_for_status()
                    with open(local_filename, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

            if not extract:
                mrich.success(f"Download complete [{iteration}]:", local_filename)
                return local_filename

            if file_url.endswith(".zip"):

                with mrich.loading(f"Unzipping [{iteration}]..."):

                    import zipfile

                    target_dir = destination / Path(file_url).name.removesuffix(".zip")

                    target_dir.mkdir(exist_ok=True)

                    mrich.writing(f"[{iteration}] {target_dir}")
                    with zipfile.ZipFile(local_filename, "r") as zip_ref:
                        zip_ref.extractall(target_dir)

            elif file_url.endswith(".tar.gz"):

                with mrich.loading(f"Expanding tarball [{iteration}]..."):

                    import tarfile

                    target_dir = destination / Path(file_url).name.removesuffix(
                        ".tar.gz"
                    )

                    target_dir.mkdir(exist_ok=True)

                    mrich.writing(f"[{iteration}] {target_dir}")
                    with tarfile.open(local_filename, "r:gz") as tar_ref:
                        tar_ref.extractall(target_dir)

            else:
                raise ValueError(f"Unsupported filetype [{iteration}]")

            mrich.success(f"Download complete [{iteration}]:", target_dir)

        else:
            # Failed to start the download
            status_code = start_download_process_response.status_code
            text = start_download_process_response.text
            mrich.error(f"Initiation of download failed [{iteration}]: code={status_code} text={text}")
            return None

    return target_dir


def target_uploads(
    stack: str = "production",
    token: str | None = None,
    statistics_only: bool = False,
) -> dict[(str,str), list]:
    """Request a dictionary of uploads keyed by target name and target_access_strings from a Fragalysis deployment

    :param stack: shorthand or URL of Fragalysis deployment, defaults to "production"
    :param token: optional authentication token
    :param statistics_only: don't list individual uploads
    :returns: list of target upload dictionaries with "id", "title", and "project" keys
    """

    from datetime import datetime

    with _session(stack, token) as session:

        # get the API response

        url = urljoin(session.root, TARGET_EXPERIMENT_UPLOADS_URL)

        response = session.get(url)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            return None

        data = response.json()

        # group the data by (target_name, proposal_number)

        formatted = {}
        for d in data["results"]:

            key = (d["target_name"], d["proposal_number"])

            formatted.setdefault(key, {})
            formatted[key].setdefault("uploads", [])

            formatted[key]["target_id"]=d["target"]
            formatted[key]["target_name"]=d["target_name"]
            formatted[key]["target_access_string"]=d["proposal_number"]
            formatted[key]["project_id"]=d["project"]

            # reformat the serialised data

            formatted[key]["uploads"].append(dict(
                xca_tarball_url=d["tarball"],
                committer_id=d["committer"],
                committer_name=d["committer_name"],
                upload_index=d["upload_version"],
                data_format=f"{d['data_version_major']}.{d['data_version_minor']}",
                timestamp=datetime.fromisoformat(d["commit_datetime"].replace("Z", "+00:00")),
            ))

    # sort and format the data

    for key, d in formatted.items():

        new_d = {}

        # general information
        new_d["target_id"]=d["target_id"]
        new_d["target_name"]=d["target_name"]
        new_d["target_access_string"]=d["target_access_string"]
        new_d["project_id"]=d["project_id"]

        # sort uploads
        sorted_uploads = sorted(d["uploads"], key=lambda d: d["upload_index"])

        # latest statistics
        new_d["last_upload_index"]=sorted_uploads[-1]["upload_index"]
        new_d["last_upload_timestamp"]=sorted_uploads[-1]["timestamp"]

        if not statistics_only:
            new_d["uploads"] = sorted_uploads

        formatted[key] = new_d

    return formatted
