# fragalysis

STACKS = {
    "staging": "https://fragalysis.xchem.diamond.ac.uk",
    "production": "https://fragalysis.diamond.ac.uk",
}

LOGIN_URL = "/accounts/login/"
DOWNLOAD_URL = "/api/download_structures/"
LANDING_PAGE_URL = "/viewer/react/landing/"
TARGETS_URL = "/api/targets/"
PROJECTS_URL = "/api/projects/"
SESSION_PROJECTS_URL = "/api/session-projects/"
SNAPSHOTS_URL = "/api/snapshots/"
JOB_TRANSFER_URL = "/api/job_file_transfer/"
JOB_REQUEST_URL = "/api/job_request/"
CSET_UPLOAD_URL = "/viewer/upload_cset/"
SITE_OBSERVATIONS_URL = "/api/site_observations"
TASK_STATUS_URL = "/viewer/task_status/"
USER_URL = "/api/user"

# data manager

DATA_MANAGERS = {
    "production": "https://data-manager-ui.xchem.diamond.ac.uk",
    "staging": "https://data-manager-ui.xchem.diamond.ac.uk",
    "dev": "https://data-manager-ui.xchem-dev.diamond.ac.uk",
}

SQUONK_DM_TASK_URL = "/data-manager-ui/api/dm-api/task/"
SQUONK_DM_INSTANCE_URL = "/data-manager-ui/api/dm-api/instance/"
