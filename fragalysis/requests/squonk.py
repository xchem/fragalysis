# data manager

DATA_MANAGERS = {
    "production": "https://data-manager-ui.xchem.diamond.ac.uk",
    "staging": "https://data-manager-ui.xchem.diamond.ac.uk",
    "dev": "https://data-manager-ui.xchem-dev.diamond.ac.uk",
}

SQUONK_DM_TASK_URL = "/data-manager-ui/api/dm-api/task/"
SQUONK_DM_INSTANCE_URL = "/data-manager-ui/api/dm-api/instance/"


def monitor_job(
    instance: str,
    token: str,
    stack: str = "production",
):

    # instance can be the full URL, just URL extension, or just the instance ID

    raise NotImplementedError


def fetch_results(
    instance: str,
    token: str,
    stack: str = "production",
):

    raise NotImplementedError
