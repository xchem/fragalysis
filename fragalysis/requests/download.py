import mrich
from pathlib import Path
from urllib.parse import urljoin

from .session import _session
from .urls import PROJECTS_URL, TARGETS_URL, DOWNLOAD_URL


def target_list(stack: str = "production", token: str | None = None) -> list[dict]:
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

        return targets


def download_target(
    name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
    destination: str = ".",
) -> None:
    """Request a target download from a Fragalysis deployment

    :param name: name of the target to request
    :param tas: target access string of the target
    :param stack: shorthand or URL of Fragalysis deployment, defaults to "production"
    :param token: optional authentication token
    :param destination: directory within which to place the download, defaults to "." (current working directory)
    """

    payload = {
        "all_aligned_structures": True,
        "cif_info": False,
        "diff_file": False,
        "event_file": False,
        "file_url": "",
        "map_info": False,
        "metadata_info": True,
        "mtz_info": False,
        "pdb_info": False,
        "proteins": "",
        "sigmaa_file": False,
        "single_sdf_file": True,
        "static_link": False,
        "target_name": name,
        "target_access_string": tas,
        "trans_matrix_info": False,
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
            file_url_response = start_download_process_response.json()

            file_url = file_url_response["file_url"]

            local_filename = destination / Path(file_url).name

            with mrich.loading("Downloading..."):

                mrich.writing(local_filename)

                with session.get(
                    download_api_url,
                    params=file_url_response,
                    stream=True,
                ) as r:

                    r.raise_for_status()
                    with open(local_filename, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

            with mrich.loading("Unzipping..."):

                import zipfile

                target_dir = destination / Path(file_url).name.removesuffix(".zip")

                target_dir.mkdir(exist_ok=True)

                mrich.writing(target_dir)
                with zipfile.ZipFile(local_filename, "r") as zip_ref:
                    zip_ref.extractall(target_dir)

                mrich.success("Download complete:", target_dir)

        else:
            mrich.error("Download Failed")
            return None

    return target_dir
