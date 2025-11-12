import time
import mrich
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_MANAGERS = {
    "production": "https://data-manager-ui.xchem.diamond.ac.uk",
    "staging": "https://data-manager-ui.xchem.diamond.ac.uk",
    "dev": "https://data-manager-ui.xchem-dev.diamond.ac.uk",
}

DM_API_URLS = {
    "production": "https://data-manager.xchem.diamond.ac.uk/data-manager-api",
    "staging": "https://data-manager.xchem.diamond.ac.uk/data-manager-api",
}

SQUONK_DM_TASK_URL = "/data-manager-ui/api/dm-api/task/"
SQUONK_DM_INSTANCE_URL = "/data-manager-ui/api/dm-api/instance/"


def projects(
    token: str,
    stack: str = "production",
) -> "pd.DataFrame":

    from squonk2.dm_api import DmApi

    DmApi.set_api_url(DM_API_URLS[stack])

    # get projects

    response = DmApi.get_available_projects(token)

    if not response.success:
        mrich.error("Failed to get projects from squonk")
        return None

    projects = response.msg["projects"]

    df = pd.DataFrame(projects)
    df = df.set_index("project_id")

    return df


def instances(
    token: str,
    stack: str = "production",
) -> "pd.DataFrame":

    from squonk2.dm_api import DmApi

    DmApi.set_api_url(DM_API_URLS[stack])

    # get projects

    response = DmApi.get_available_instances(token)

    if not response.success:
        mrich.error("Failed to get instances from squonk. Is token valid?")
        return None

    instances = response.msg["instances"]

    df = pd.DataFrame(instances)
    df = df.set_index("id")

    return df


def monitor_jobs(
    token: str,
    stack: str = "production",
    instance_ids: str | list[str] | None = None,
    applications: bool = False,
    pending: bool = False,
):

    from mrich import console
    from rich.table import Table
    from rich.live import Live

    def get_filtered_df(
        instance_ids,
        applications,
        pending,
    ):

        df = instances(token=token, stack=stack)

        if df is None:
            return None

        if instance_ids:
            if isinstance(instance_ids, str):
                instance_ids = [instance_ids]
            df = df.loc[instance_ids]

        if not applications:
            df = df[~(df["application_type"] == "APPLICATION")]

        if not pending:
            df = df[~(df["phase"] == "PENDING")]

        return df

    def job_table(df):
        table = Table(title=f"Squonk Jobs ({datetime.now()})")

        table.add_column("Instance", justify="left", no_wrap=True)
        table.add_column("Job Type", justify="left", no_wrap=True)
        # table.add_column("Name", justify="left", no_wrap=False)
        table.add_column("Run Time", justify="right")
        table.add_column("Status", justify="center")

        if df is not None:
            for i, row in df.iterrows():
                table.add_row(
                    str(i),
                    str(row["job_job"]),
                    # str(row["name"]),
                    str(row["run_time"]),
                    str(row["phase"]),
                )

        return table

    try:
        df = get_filtered_df(instance_ids, applications, pending)
        with Live(job_table(df), refresh_per_second=1, console=console) as live:
            while True:
                df = get_filtered_df(instance_ids, applications, pending)
                live.update(job_table(df))
                time.sleep(1)

    except KeyboardInterrupt:
        pass

    return None


def list_files(
    instance: str,
    token: str,
    stack: str = "production",
    root: str = "/",
):

    from squonk2.dm_api import DmApi

    df = instances(
        stack=stack,
        token=token,
    )

    project_id = df.loc[instance]["project_id"]
    mrich.var("project_id", project_id)

    DmApi.set_api_url(DM_API_URLS[stack])

    if not root.startswith("/"):
        root = "/" + root

    def project_tree(root="/"):
        response = DmApi.list_project_files(
            token, project_id=project_id, project_path=root
        )

        if not response.success:
            mrich.error("Failed to get project files")
            raise ValueError

        path = response.msg["path"]
        paths = response.msg["paths"]
        files = response.msg["files"]

        filepaths = [str(Path(path) / f["file_name"]) for f in files]

        for subpath in paths:
            subpath = str(Path(path) / subpath)
            filepaths.extend(project_tree(subpath))

        return filepaths

    # search whole tree
    with mrich.loading("Getting project files..."):
        files = project_tree(root)

    return sorted(files)


def get_file(
    instance: str,
    path: str,
    token: str,
    stack: str = "production",
    destination: str = None,
):

    from squonk2.dm_api import DmApi

    df = instances(
        stack=stack,
        token=token,
    )

    project_id = df.loc[instance]["project_id"]
    mrich.var("project_id", project_id)

    DmApi.set_api_url(DM_API_URLS[stack])

    if not path.startswith("/"):
        path = "/" + path

    path = Path(path)
    parent = str(path.parent)
    file = path.name


    if not destination:
        destination = file
    elif destination.endswith("/"):
        destination = Path(destination) / file
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination = str(destination)

    response = DmApi.get_unmanaged_project_file(
        token,
        project_id=project_id,
        project_path=parent,
        project_file=file,
        local_file=destination,
    )

    if not response.success:
        mrich.error("Failed to get file", response)
        # raise ValueError
        return None

    mrich.writing(destination)


def human_timedelta(delta):

    bits = []

    if delta.days < 0 or delta.seconds < 0:
        return ""

    days = delta.days

    s = delta.seconds

    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    if days:
        bits.append(f"{days}d")

    if h:
        bits.append(f"{h}h")

    if m:
        bits.append(f"{m}m")

    if s:
        bits.append(f"{s}s")

    bits = (str(b) for b in bits)

    return " ".join(bits)
