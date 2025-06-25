import mrich
from mrich import print

import pandas as pd
from urllib.parse import urljoin, quote

from .session import _session
from .urls import SESSION_PROJECTS_URL, SNAPSHOTS_URL, JOB_TRANSFER_URL

"""

0. Ensure job over-rides exist on stack (/api/job_override)
1. Create session project (/api/session-projects/)
2. Create snapshot (/api/snapshots/)
3. Transfer snapshot (/api/job_file_transfer/)

"""


def transfer_snapshot(
    token: str,
    snapshot_id: int,
    session_project_id: int,
    target_id: int,
    stack: str = "production",
):

    payload = dict(
        snapshot=snapshot_id,
        session_project=session_project_id,
        access=2,  # ???
        target=target_id,
        # squonk_project= ???, # e.g. "project-8f32b412-8329-4469-a39c-8581efa93796",
        proteins=quote(
            "target_loader_data/Flavi_NS5_RdRp_lb32627-71/upload_1/aligned_files/DNV2_NS5A-x0135/DNV2_NS5A-x0135_A_1608_1_DNV2_NS5A-x0135+A+1608+1_apo-desolv.pdb"
        ),
        # compounds="target_loader_data/CoV-Mpro_lb32627-71/upload_1/aligned_files/5r7y/5r7y_A_1001_1_7gbd%2BA%2B404%2B1_ligand.mol,target_loader_data/CoV-Mpro_lb32627-71/upload_1/aligned_files/5r7z/5r7z_A_404_1_7gbd%2BA%2B404%2B1_ligand.mol",
    )

    # target_loader_data/Flavi_NS5_RdRp_lb32627-71_3/upload_1/aligned_files/DNV2_NS5A-x0288/DNV2_NS5A-x0288_A_1701_1_DNV2_NS5A-x0288%2BA%2B1701%2B1_apo-desolv.pdb

    with _session(stack, token) as session:

        mrich.print(payload)

        url = urljoin(session.root, JOB_TRANSFER_URL)
        response = session.post(url, data=payload)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
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
):

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

        mrich.print(payload)

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

        # print( sps)

    df = pd.DataFrame(sps["results"])
    return df.sort_values(by="init_date").iloc[-1]["id"]
