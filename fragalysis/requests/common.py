import mrich
from mrich import print

from urllib.parse import urljoin

from .session import _session
from .urls import SITE_OBSERVATIONS_URL, USER_URL


def user_info(
    stack: str = "production",
    token: str | None = None,
) -> dict:

    with _session(stack, token) as session:

        url = urljoin(session.root, USER_URL)

        response = session.post(url)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            return None

        try:
            json = response.json()
        except Exception as e:
            mrich.error("Can't get user info, is token valid?")
            return None

        return json


def site_observations(
    target_id: int | None = None,
    stack: str = "production",
    token: str | None = None,
) -> dict:

    with _session(stack, token) as session:

        url = urljoin(session.root, SITE_OBSERVATIONS_URL)

        if target_id:
            response = session.post(url, params=dict(target=target_id))
        else:
            response = session.post(url)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            return None

        json = response.json()

        return json["results"]
