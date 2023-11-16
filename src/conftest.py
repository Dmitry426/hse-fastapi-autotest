import json
import logging
from functools import lru_cache
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
import yaml

from src.helpers.repo_getter import traverse_and_import

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

path = Path(__file__).parent
app = traverse_and_import(path)


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


@lru_cache(maxsize=None)
def reference_schema():
    with open((path / 'test_data/reference.json'), 'r') as json_file:
        data_from_file = json.load(json_file)
        return data_from_file


@pytest.fixture(scope='module')
def openapi_schema(client):
    response = client.get("/openapi.yaml")
    if response.status_code != 200:
        response = client.get("/openapi.json")
    yield yaml.safe_load(response.text)



