import pytest

from src.conftest import logger, reference_schema


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


@pytest.mark.parametrize("test_data", reference_schema()['paths'])
def test_generated_tests(client, test_data, openapi_schema):
    reference = reference_schema()['paths']
    test = openapi_schema['paths']
    try:
        methods_reference = list(reference[test_data])
        test_methods = list(test[test_data])
        assert methods_reference == test_methods
        logger.info(f"Референс методы {test_data} совпадают"
                    f" с методами тест объекта  ")
    except KeyError:
        logger.info(f"Путь {test_data} не реализован в тест"
                    f" объекте либо имеет другое название и параметры ")
        return
    for method in methods_reference:
        resp = list(reference[test_data][method]['responses'])
        try:
            params = reference[test_data][method]['parameters']
            if isinstance(params, list):
                req = params[0]
        except KeyError:
            params = None
            req = None
        print(req)
