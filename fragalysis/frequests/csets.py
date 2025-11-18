"""Upload SDFs to RHS"""

import mrich
from pathlib import Path
from urllib.parse import urljoin

from .session import _session
from .urls import CSET_UPLOAD_URL


def upload_sdf(
    token: str,
    target_name: str,
    tas: str,
    sdf_file: str | Path,
    *,
    stack: str = "production"
):

    sdf_file = Path(sdf_file)
    assert sdf_file.exists()

    with open(sdf_file, "rb") as f:
        sdf_data = f.read()

    with _session(stack, token) as session:


        payload = dict(
            target_name=target_name,
            proposal_ref=tas,
            submit_choice="U",
            update_set=None,
        )
        
        url = urljoin(session.root, CSET_UPLOAD_URL)
        print(url)

        print(payload)
        payload["sdf_file"] = sdf_data,
        
        response = session.post(url, data=payload)

    if not response.ok:
        mrich.error("Request failed", url, response.status_code)
        mrich.print(response.text)
        return None

    mrich.success("Uploaded successfully")
    return response
