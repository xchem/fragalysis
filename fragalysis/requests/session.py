import mrich
from urllib.parse import urljoin
from pathlib import Path
from .urls import STACKS, LANDING_PAGE_URL

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


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

    response = session.get(landing_page_url)  # sets csrftoken

    assert response.ok

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
