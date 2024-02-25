from typing import Dict

import pytest

from hse_fastapi_autotest.conftest import reference_schema
from hse_fastapi_autotest.services.generators.body_generator import BodyGenerator
from hse_fastapi_autotest.services.generators.param_generator import ParamGenerator
from hse_fastapi_autotest.services.shema_parsers.testing_metadata_parser import (
    PathMethodCombinations,
    get_operation,
    get_request_body_schema,
    get_response_codes,
)


class TestEndToEnd:
    specification = reference_schema()

    @pytest.mark.parametrize(
        "valid_path, valid_method",
        PathMethodCombinations(specification).valid_path_method_combinations(),
    )
    def test_e2e(self, client, valid_path, valid_method):
        operation = get_operation(self.specification, valid_method, valid_path)

        responses = get_response_codes(operation.responses)

        generated_params = ParamGenerator().generate_parameters_dict(
            operation.parameters
        )
        request_body_schema = get_request_body_schema(operation)
        generated_body = BodyGenerator().generate_body_dict(request_body_schema)

        if self.ensure_path_parameter:
            valid_path = self.add_path_parameters(valid_path, generated_params)

        response = client.request(
            valid_method.value, valid_path, json=generated_body, params=generated_params
        )

        assert response.status_code == responses["positive_responses"][0]

    @staticmethod
    def ensure_path_parameter(valid_path: str):
        if "{" in valid_path and "}" in valid_path:
            return True
        return False

    @staticmethod
    def add_path_parameters(valid_path: str, parameters: Dict):
        return valid_path.format(**parameters)
