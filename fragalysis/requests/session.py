import logging
from http.client import HTTPConnection
import requests
from urllib.parse import urljoin

from .urls import STACKS, LANDING_PAGE_URL

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def debug_requests_on(context_id: int = 1):
    """Switches requests module logging on"""
    HTTPConnection.debuglevel = 1

    logging.basicConfig(
        format=f"[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] # [{context_id}] %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
    )
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def _session(stack: str = "production", token: str | None = None):

    url_root = STACKS[stack] if stack in STACKS else stack
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

    if csrftoken := session.cookies.get("csrftoken", None):
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
