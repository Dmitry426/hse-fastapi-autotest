import logging
from pathlib import Path
from urllib.parse import urlparse

from hse_fastapi_autotest import PROJECT_ROOT

logger = logging.getLogger(__name__)


def extract_repo_name(repo_url: str) -> str:
    """Extract the repository name from the GitHub URL."""
    parsed_url = urlparse(repo_url)
    path_segments = parsed_url.path.strip("/").split("/")
    return path_segments[-2] + "_" + path_segments[-1].replace(".git", "")


def ensure_path(path: str | Path, project_root: Path = PROJECT_ROOT) -> Path:
    """
    Ensure that the given path exists and is
    absolute or relative to the project root.
    """
    path = Path(path)

    if path.is_absolute():
        return path
    relative = project_root / path
    return relative
