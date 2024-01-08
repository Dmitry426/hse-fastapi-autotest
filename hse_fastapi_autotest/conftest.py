import json
from functools import lru_cache
from pathlib import Path
from typing import Dict

import pytest
from fastapi.testclient import TestClient
import yaml

from hse_fastapi_autotest.services.app_finder import traverse_and_import

path = Path(__file__).parent
app = traverse_and_import(path)


@pytest.fixture(scope='module')
def client() -> TestClient:
    """Fast api test client"""
    yield TestClient(app)


@lru_cache(maxsize=None)
def reference_schema() -> Dict:
    """Get reference schema  """
    with open((path / 'test_data/reference.json'), 'r') as json_file:
        data_from_file = json.load(json_file)
        return data_from_file


@pytest.fixture(scope='module')
def openapi_schema(client) -> Dict:
    """Get fast api  openapi schema  """
    response = client.get("/openapi.yaml")
    if response.status_code != 200:
        response = client.get("/openapi.json")
    yield yaml.safe_load(response.text)
