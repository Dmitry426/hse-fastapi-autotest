
from typing import Dict, List

import pytest
from openapi_parser.enumeration import OperationMethod
from openapi_parser.specification import Operation, Response, Specification

from hse_fastapi_autotest.conftest import client, reference_schema, openapi_schema
from hse_fastapi_autotest.services.generators.body_generator import BodyGenerator
from hse_fastapi_autotest.services.generators.param_generator import ParamGenerator
from hse_fastapi_autotest.services.test_path_parser import PathMethodCombinations


def get_operation(spec: Specification, method: OperationMethod,
                  path: str) -> Operation | None:
    """
    Get the parameters for a specific method and path from the OpenAPI specification.

    Args:
        spec (Specification): The OpenAPI parsed  specification.
        method (OperationMethod): The HTTP method (e.g., 'GET', 'POST') for
        the operation.
        path (str): The path for the operation.

    Returns:
        list: A list of parameters for the specified method and path.
    """
    for path_item in spec.paths:
        if path_item.url == path:
            for operation in path_item.operations:
                if operation.method == method:
                    return operation
    return None


def get_response_codes(spec: List[Response]) -> Dict[str, List]:
    """
    Get positive and negative response codes from the given list of responses.

    Parameters:
        spec (List[Response]): List of responses from the OpenAPI schema.

    Returns:
        Dict[str, List[int]]: Dictionary containing lists of positive and negative
        response codes.
    """
    positive_responses = set()
    negative_responses = set()

    for response in spec:
        code = response.code
        if 200 <= code < 300:
            positive_responses.add(code)
        elif 400 <= code < 600:
            negative_responses.add(code)

    return {'positive_responses': list(positive_responses),
            'negative_responses': list(negative_responses)}


def get_request_body_schema(operation):
    """
    Get the request body schema from the OpenAPI Operation.

    Parameters:
        operation: OpenAPI Operation object.

    Returns:
        dict or None: The request body schema as a dictionary or None if not found.
    """
    if operation.request_body and operation.request_body.content:
        for content_item in operation.request_body.content:
            return content_item.schema

    return None


def ensure_path_parameter(valid_path: str):
    if '{' in valid_path and '}' in valid_path:
        return True
    return False


def add_path_parameters(valid_path: str, parameters: Dict):
    return valid_path.format(**parameters)


class TestEndToEnd:
    specification = reference_schema()

    @pytest.mark.parametrize("valid_path, valid_method",
                             PathMethodCombinations(specification).
                             valid_path_method_combinations())
    def test_e2e(self, client, openapi_schema, valid_path, valid_method):
        operation = get_operation(self.specification, valid_method, valid_path)
        responses = get_response_codes(operation.responses)
        params = operation.parameters
        generated_params = ParamGenerator().generate_parameters_dict(params)
        request_body_schema = get_request_body_schema(operation)
        generated_body = BodyGenerator().generate_body_dict(request_body_schema)

        if ensure_path_parameter:
            valid_path = add_path_parameters(valid_path, generated_params)
        response = client.request(valid_method.value,
                                  valid_path
                                  , json=generated_body,
                                  params=generated_params)

        assert response.status_code == responses['positive_responses'][0]
