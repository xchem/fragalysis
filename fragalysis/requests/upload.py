"""Upload SDFs to RHS"""

import mrich
from pathlib import Path
from urllib.parse import urljoin

from .session import _session
from .urls import CSET_UPLOAD_URL


def upload_sdf(
    token: str,
    target_name: str,
    target_access_string: str,
    sdf_file: str | Path,
    *,
    stack: str = "production"
):

    sdf_file = Path(sdf_file)
    assert sdf_file.exists()

    payload = dict(
        target_name=target_name,
        proposal_ref=target_access_string,
        # sdf_file=..., #process the file into binary
        submit_choice="U",
        update_set=None,
    )

    files = {
        "sdf_file": (sdf_file.name, open(sdf_file, "rb"), "application/octet-stream"),
    }

    with _session(stack, token) as session:
        url = urljoin(session.root, CSET_UPLOAD_URL)
        response = session.post(url, data=payload, files=files)

    files["sdf_file"][1].close()

    if not response.ok:
        mrich.error("Request failed", url, response.status_code)
        mrich.print(response.text)
        return None

    mrich.success("Uploaded successfully")
    return response
