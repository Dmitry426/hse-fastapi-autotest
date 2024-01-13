from typing import List, Tuple

from openapi_parser.enumeration import OperationMethod
from openapi_parser.specification import Specification


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
        return [OperationMethod.GET, OperationMethod.POST, OperationMethod.PUT,
                OperationMethod.DELETE, OperationMethod.PATCH,
                OperationMethod.HEAD, OperationMethod.OPTIONS]

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
