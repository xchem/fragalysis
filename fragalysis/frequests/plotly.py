import mrich

from urllib.parse import urljoin

from .session import _session
from .urls import PLOT_DATA_URL

# push to plot_data endpoint


def upload_graph(
    title: str,
    figure: "go.Figure",
    target_name: str,
    tas: str,
    stack: str = "production",
    token: str | None = None,
    identifier: str = "observation_code",
):
    """Upload a plotly.graph_objects.Figure to the Fragalysis RHS"""

    from .download import target_list

    mrich.var("target_name", target_name)
    mrich.var("tas", tas)
    mrich.var("stack", stack)
    mrich.var("identifier", identifier)

    assert identifier in ["observation_code", "compound_code", "computed_molecule_code"]

    # GET TARGET AND PROJECT INFO

    targets, projects = target_list(stack=stack, token=token, return_project_data=True)

    for target_id, name, proposal in targets:
        if name == target_name and proposal == tas:
            break
    else:
        mrich.error("Target not found", target_name, tas)
        return None

    mrich.var("target_id", target_id)

    for project_id, proposal in projects.items():
        if proposal == tas:
            break

    mrich.var("project_id", project_id)

    # CHECK THE GRAPH

    if any(trace.customdata is None for trace in figure.data):
        mrich.warning(
            "No traces have custom data defined, Fragalysis on-click events won't work"
        )

    # FORMAT THE PAYLOAD

    payload = dict(
        title=title,
        plotly_data=figure.to_json(),
        notebook_path=None,
        squonk_project_id=None,
        target=target_id,
        project=project_id,
        identifier=identifier,
    )

    # PUSH THE GRAPH

    with _session(stack=stack, token=token) as session:

        url = urljoin(session.root, PLOT_DATA_URL)

        print(url)

        response = session.post(url, data=payload)

        if not response.ok:
            mrich.error("Request failed", url, response.status_code)
            mrich.print(response.text)
            return None

        mrich.success("Graph uploaded w/ id", response.json()["id"])
