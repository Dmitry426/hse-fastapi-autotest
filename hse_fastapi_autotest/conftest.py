import logging
import os
import shutil
from functools import lru_cache
from pathlib import Path
from typing import Dict

import pytest
import yaml
from fastapi.testclient import TestClient
from git import GitCommandError, Repo
from openapi_parser import parse
from openapi_parser.parser import _create_parser
from openapi_parser.specification import Specification

from hse_fastapi_autotest import PROJECT_ROOT
from hse_fastapi_autotest.services.finders.app_finder import traverse_and_import
from hse_fastapi_autotest.services.helpers.utils import ensure_path, extract_repo_name

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("fastapi_autotest")


def pytest_addoption(parser):
    parser.addoption("--repo_url", action="store", help="Git repository URL")
    parser.addoption(
        "--tested_app_dir",
        action="store",
        default="temp_repos",
        help="Tested app directory " "destination",
    )


def clone_repository(repo_url, destination_path):
    try:
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        repo = Repo.clone_from(repo_url, destination_path)
        return repo
    except GitCommandError as e:
        logger.info(f"GitCommandError: {e}")
        raise e


@pytest.fixture(scope="session")
def git_repo(request):
    """Fixture to load a Git repository."""
    repo_url = request.config.getoption("--repo_url")
    tested_app_dir = request.config.getoption("--tested_app_dir")
    if not repo_url:
        pytest.exit("Please provide the Git repository URL.")

    repo_name = extract_repo_name(repo_url)
    logger.info(f"Using Git repository URL: {repo_url}")

    destination = ensure_path(Path(tested_app_dir) / repo_name)

    repo = clone_repository(repo_url, destination)
    yield repo


@pytest.fixture(scope="session")
def test_directory(git_repo):
    """Fixture to define the test directory based on the loaded Git repository."""
    return Path(git_repo.working_dir)


@pytest.fixture(scope="module")
def client(test_directory) -> TestClient:
    """Fast api test client"""
    app = traverse_and_import(test_directory)
    yield TestClient(app)


@lru_cache(maxsize=None)
def reference_schema() -> Specification:
    """Get reference schema"""
    specification = parse(
        str(PROJECT_ROOT / "hse_fastapi_autotest" / "config" / "openapi.json")
    )
    return specification


@pytest.fixture(scope="module")
def openapi_schema(client) -> Dict:
    """Get fast api  openapi schema"""
    response = client.get("/openapi.yaml")
    if response.status_code != 200:
        response = client.get("/openapi.json")
    parser = _create_parser(strict_enum=True)
    spec = yaml.safe_load(response.text)
    yield parser.load_specification(spec)
