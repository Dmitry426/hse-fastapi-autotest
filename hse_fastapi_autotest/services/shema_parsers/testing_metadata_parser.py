from typing import Any, Dict, List, Tuple, Union

from fastapi.openapi.models import Operation
from openapi_parser.enumeration import OperationMethod
from openapi_parser.specification import Response, Specification


def get_operation(
    spec: Specification, method: OperationMethod, path: str
) -> Operation | None:
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


def get_response_codes(spec: [Dict[str, Union[Response, Any]]]) -> Dict[str, List]:
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

    return {
        "positive_responses": list(positive_responses),
        "negative_responses": list(negative_responses),
    }


class PathMethodCombinations:
    """
    Class gives valid combinations of paths and methods for proper testing
    parametrization.
    """

    def __init__(self, specification: Specification):
        self.specification = specification

    def get_methods(self, test_data: str) -> List[OperationMethod]:
        """
        Get the list of HTTP methods for a given path.

        Parameters:
        - test_data (str): The path for which to retrieve methods.

        Returns:
        List[OperationMethod]: The list of HTTP methods for the given path.
        """
        methods_for_path = [
            operation.method
            for path in self.specification.paths
            if path.url == test_data
            for operation in path.operations
        ]
        return methods_for_path

    def valid_paths(self) -> List[str]:
        """
        Get the list of valid paths from the specification.

        Returns:
        List[str]: The list of valid paths.
        """
        return [path.url for path in self.specification.paths]

    @staticmethod
    def valid_methods() -> List[OperationMethod]:
        """
        Get the list of valid HTTP methods. Fell free to add methods

        Returns:
        List[OperationMethod]: The list of valid HTTP methods.
        """
        return [
            OperationMethod.GET,
            OperationMethod.POST,
            OperationMethod.PUT,
            OperationMethod.DELETE,
            OperationMethod.PATCH,
            OperationMethod.HEAD,
            OperationMethod.OPTIONS,
        ]

    def valid_path_method_combinations(self) -> List[Tuple[str, OperationMethod]]:
        """
        Get the list of valid path-method combinations from a given schema.

        Returns:
        List[Tuple[str, OperationMethod]]: The list of valid path-method combinations.
        """
        return [
            (path, method)
            for path in self.valid_paths()
            for method in self.valid_methods()
            if method in self.get_methods(path)
        ]
