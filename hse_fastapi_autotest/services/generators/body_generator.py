from typing import Any

from openapi_parser.specification import Property, Schema

from hse_fastapi_autotest.services.generators.base_generator import BaseGenerator


class BodyGenerator(BaseGenerator):
    def generate_body(self, schema: Property) -> Any:
        """
        Generate a request body value based on the provided schema.

        Parameters:
            schema (Property): The schema.

        Returns:
            Any : The generated request body value.
        """
        return self.generate_random_value(schema.schema.type, schema.schema.enum)

    def generate_body_dict(self, schema: Schema) -> dict | None:
        """
        Generate a dictionary containing parameters based on the provided
        schema.

        Parameters:
            schema (Schema): The schema.

        Returns:
            dict: Dictionary containing generated parameters.
        """
        generated_params = {}
        if schema:
            for property_schema in schema.properties:
                param_name = property_schema.name
                param_value = self.generate_body(property_schema)
                generated_params[param_name] = param_value

            return generated_params
        return None
