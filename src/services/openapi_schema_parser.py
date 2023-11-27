__all__ = "OpenApiParser"

from typing import Dict, Union

from src.conftest import reference_schema
from src.services.abstract_schema_parser import AbstractOpenApiParser
from src.settings.loggger import logger


class OpenApiParser(AbstractOpenApiParser):
    """Parse openapi json to a more convenient and usable representation """

    def _get_nested_schema_components(self, body_schema: Dict) -> Dict:
        """Parse nested property schema  if we have one """

        try:
            props = {}
            if body_schema.get('required', None):

                for prop in body_schema['required']:
                    ref = body_schema['properties'][prop].get('$ref', None)
                    if ref:
                        component_ref = self._get_schema_components(schema=ref)
                        props = {prop: component_ref}

            body_prop = body_schema.get('properties', None)
            if body_prop and body_prop.get('detail', None):
                items = body_schema['properties']['detail']['items']
                ref = items.get('$ref', None)
                if ref:
                    component_ref = self._get_schema_components(schema=ref)
                    props = {'err': component_ref}

            return props
        except KeyError:
            logger.error(f"Ошибка поиска вложенных $ref в  {body_schema}")

    @staticmethod
    def _get_schema_components(schema: str) -> Union[Dict, None]:
        """Get any schema from openapi components"""

        schema_name = schema.split('/')[-1]
        try:
            schemas = reference_schema()['components']['schemas'][schema_name]
        except KeyError:
            logger.error(f'В конфиге отсутствует схема {schema_name} ')
            schemas = None
        return schemas

    def _get_response(self, responses: Dict, resp) -> Union[Dict, None]:
        try:
            parsed_response = {"response": resp}
            content = responses[resp].get('content', None)
            content_type = list(content)
            schema = content.get(content_type[0], {})

            if not schema:
                logger.error(f"Схема не поддерживается  {content_type}")

            if schema['schema'].get('type', None):

                parsed_response['response_type'] = schema['schema'].get('type', None)
                if schema['schema'].get('items', None):
                    content_schema = self._get_schema_components(
                        schema['schema']['items']['$ref'])

                    props = content_schema['properties']
                    nested_ref = self._get_nested_schema_components(content_schema)
                    if nested_ref:
                        prop = {**props, **nested_ref}
                        parsed_response = {**parsed_response, **prop}

            if schema['schema'].get('$ref', None):
                content_schema = self._get_schema_components(schema['schema']['$ref'])
                props = content_schema['properties']
                nested_ref = self._get_nested_schema_components(content_schema)
                if nested_ref:
                    prop = {**props, **nested_ref}
                    parsed_response = {**parsed_response, **prop}

            return parsed_response

        except (KeyError, IndexError):
            logger.error(f"Ошибка получения {responses}")

    def parse_params(self, params):

        params_schema = {}

        if isinstance(params, list) and params:
            req = params[0]
            params_schema['place_in'] = req.get('in', None)
            params_schema['required'] = req.get('required', None)
            schema = req.get('schema', None)
            all_off_schema = schema.get('allOf', [])

            if all_off_schema:
                schema = self._get_schema_components(all_off_schema[0]['$ref'])

            return {**params_schema, **schema}

        return None

    def parse_request_body(self, request_body):
        if not request_body:
            return None
        try:
            schema = request_body['content']['application/json']['schema']['$ref']
            body_schema = self._get_schema_components(schema=schema)
            required = body_schema.get('required', None)

            if required:
                properties = body_schema.get('properties', {})
                properties['required'] = required
                ref_props = self._get_nested_schema_components(
                    body_schema=body_schema
                )
                if ref_props:
                    properties = {**properties, **ref_props}
                return properties

        except KeyError:
            logger.error(f"Ошибка парсинга схемы тела запроса {request_body} ")
        return None

    def parse_responses(self, responses):
        result = []
        for resp in responses:
            result.append(self._get_response(responses, resp))
        return result
