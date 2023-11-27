from typing import Dict

import pytest

from src.services.openapi_schema_parser import OpenApiParser
from src.settings.loggger import logger
from src.conftest import client, reference_schema, openapi_schema


class TestEndToEnd:

    @staticmethod
    def parse_openapi_reference(reference_api: Dict, test_data: str,
                                method: str) -> Dict:
        parsed_schema = {}
        method_data = reference_api[test_data][method]
        parser = OpenApiParser()

        parsed_schema['params'] = parser.parse_params(method_data.get('parameters', []))
        parsed_schema['responses'] = parser.parse_responses(
            method_data.get('responses', {}))
        parsed_schema['body'] = parser.parse_request_body(
            method_data.get('requestBody', {}))

        return parsed_schema

    @pytest.mark.parametrize("test_data", reference_schema()['paths'])
    def test_e2e(self, client, test_data, openapi_schema):
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
            schemas = self.parse_openapi_reference(
                reference_api=reference,
                test_data=test_data,
                method=method)
            print(schemas)

            if not schemas['params'] and not schemas['body']:
                logger.info(f"Сквозной тест пути:{method} и  метода:{method} ")
                resp = client.build_request(url=test_data, method=method)
                print(resp.__dict__)
