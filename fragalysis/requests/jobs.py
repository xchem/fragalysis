import mrich
from mrich import print

from pathlib import Path
from urllib.parse import urljoin, quote, unquote

from .session import _session
from .urls import (
    SESSION_PROJECTS_URL,
    SNAPSHOTS_URL,
    JOB_TRANSFER_URL,
)


def transfer_snapshot(
    token: str,
    snapshot_id: int,
    session_project_id: int,
    target_id: int,
    protein_files: list[str] | None = None,
    compound_files: list[str] | None = None,
    stack: str = "production",
):

    payload = dict(
        snapshot=snapshot_id,
        session_project=session_project_id,
        access=2,
        target=target_id,
    )

    if compound_files:
        compounds = ",".join(compound_files)
    else:
        compounds = ""

    payload["compounds"] = compounds

    if protein_files:
        proteins = ",".join(protein_files)
    else:
        proteins = ""

    payload["proteins"] = proteins

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


def modify_filepath(path, transfer_root):
    return str(Path(transfer_root) / Path(path).name)
