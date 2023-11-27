from src.conftest import client, reference_schema, openapi_schema


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200


def test_openapi_schema_info(openapi_schema):
    assert "info" in openapi_schema
    assert "title" in openapi_schema["info"]
    assert "version" in openapi_schema["info"]


def test_openapi_schema_paths(openapi_schema):
    assert "paths" in openapi_schema
    assert "/" in openapi_schema["paths"]
    assert openapi_schema["paths"] == reference_schema()["paths"]
