import json
from functools import lru_cache
from pathlib import Path
from typing import Dict

import pytest
from fastapi.testclient import TestClient
import yaml
from openapi_parser import parse
from openapi_parser.parser import _create_parser
from openapi_parser.specification import Specification

from hse_fastapi_autotest import PROJECT_ROOT
from hse_fastapi_autotest.services.app_finder import traverse_and_import
from hse_fastapi_autotest.services.test_path_parser import PathMethodCombinations

path = Path(__file__).parent
app = traverse_and_import(path)


@pytest.fixture(scope='module')
def client() -> TestClient:
    """Fast api test client"""
    yield TestClient(app)


@lru_cache(maxsize=None)
def reference_schema() -> Specification:
    """Get reference schema  """
    specification = parse(str(PROJECT_ROOT / "test_data" / "reference.json"))
    return specification


@pytest.fixture(scope='module')
def openapi_schema(client) -> Dict:
    """Get fast api  openapi schema  """
    response = client.get("/openapi.yaml")
    if response.status_code != 200:
        response = client.get("/openapi.json")
    parser = _create_parser(strict_enum=True)
    spec = yaml.safe_load(response.text)
    yield parser.load_specification(spec)


