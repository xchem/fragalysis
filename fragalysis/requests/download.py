import re
import time
import mrich

from pathlib import Path
from json import JSONDecodeError
from urllib.parse import urljoin

from .session import _session
from .urls import PROJECTS_URL, TARGETS_URL, DOWNLOAD_URL


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
    assert destination.exists()

    with _session(stack, token) as session:

        download_api_url = urljoin(session.root, DOWNLOAD_URL)

        with mrich.loading("Requesting download"):

            start_download_process_response = session.post(
                download_api_url,
                data=payload,
            )

        if start_download_process_response.ok:
            response_json = start_download_process_response.json()

            task_status_url = response_json.get("task_status_url")

            if not task_status_url:
                raise ValueError("No task URL returned")

            ### CONTINUOUSLY MONITOR DOWNLOAD TASK

            task_status_url = urljoin(session.root, task_status_url)

            with mrich.loading("Preparing download"):
                for i in range(100_000):

                    status = session.get(task_status_url)

                    try:
                        status_json = status.json()
                    except JSONDecodeError:
                        continue

                    started = status_json.get("started", False)
                    finished = status_json.get("finished", False)

                    if finished:
                        break

                    time.sleep(0.5)

                else:
                    mrich.error("Timed out")
                    raise ValueError

            file_url = status_json.get("messages", "")

            if not re.search(r"^\/code\/media\/downloads\/.*\.tar\.gz$", file_url):
                mrich.error("No tarball in payload")

            ### DOWNLOAD PREPARED PAYLOAD

            local_filename = destination / Path(file_url).name

            with mrich.loading("Downloading..."):

                mrich.writing(local_filename)

                with session.get(
                    download_api_url,
                    params=dict(file_url=file_url),
                    stream=True,
                ) as r:

                    r.raise_for_status()
                    with open(local_filename, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

            if file_url.endswith(".zip"):

                with mrich.loading("Unzipping..."):

                    import zipfile

                    target_dir = destination / Path(file_url).name.removesuffix(".zip")

                    target_dir.mkdir(exist_ok=True)

                    mrich.writing(target_dir)
                    with zipfile.ZipFile(local_filename, "r") as zip_ref:
                        zip_ref.extractall(target_dir)

            elif file_url.endswith(".tar.gz"):

                with mrich.loading("Expanding tarball..."):

                    import tarfile

                    target_dir = destination / Path(file_url).name.removesuffix(
                        ".tar.gz"
                    )

                    target_dir.mkdir(exist_ok=True)

                    mrich.writing(target_dir)
                    with tarfile.open(local_filename, "r:gz") as tar_ref:
                        tar_ref.extractall(target_dir)

            else:
                raise ValueError("Unsupported filetype")

            mrich.success("Download complete:", target_dir)

        else:
            mrich.error("Download Failed")
            return None

    return target_dir
