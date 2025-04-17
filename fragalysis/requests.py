import mrich
from urllib.parse import urljoin
from pathlib import Path

STACKS = {
    "staging": "https://fragalysis.xchem.diamond.ac.uk",
    "production": "https://fragalysis.diamond.ac.uk",
}
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

LOGIN_URL = "/accounts/login/"
DOWNLOAD_URL = "/api/download_structures/"
LANDING_PAGE_URL = "/viewer/react/landing/"
TARGETS_URL = "/api/targets/"
PROJECTS_URL = "/api/projects/"


def _session(stack: str = "production", token: str | None = None):

    import requests

    if stack in STACKS:
        url_root = STACKS[stack]
    else:
        url_root = stack

    landing_page_url = urljoin(url_root, LANDING_PAGE_URL)

    session = requests.Session()
    session.root = url_root

    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Referer": landing_page_url,
            "Referrer-policy": "same-origin",
        }
    )

    session.get(landing_page_url)  # sets csrftoken

    # set manually if still missing
    csrftoken = session.cookies.get("csrftoken", None)
    if csrftoken:
        session.headers.update(
            {
                "X-CSRFToken": csrftoken,
                "User-Agent": USER_AGENT,
            }
        )

    if token:
        session.cookies.update(
            {
                "sessionid": token,
            }
        )

    return session


def target_list(stack: str = "production", token: str | None = None):

    with _session(stack, token) as session:

        # projects
        projects_url = urljoin(session.root, PROJECTS_URL)
        project_response = session.get(projects_url)

        if not project_response.ok:
            mrich.error("Response failed", projects_url, project_response.status_code)
            return None

        # targets
        targets_url = urljoin(session.root, TARGETS_URL)
        target_response = session.get(targets_url)

        if not target_response.ok:
            mrich.error("Response failed", targets_url, target_response.status_code)
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
):

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