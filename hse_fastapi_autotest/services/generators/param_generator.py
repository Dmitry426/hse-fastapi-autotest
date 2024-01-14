from typing import Any, List, Optional

from openapi_parser.specification import Parameter

from hse_fastapi_autotest.services.generators.base_generator import BaseGenerator


class ParamGenerator(BaseGenerator):
    def generate_parameter(
        self, param: Parameter, selected_value: Optional[Any] = None
    ) -> Any:
        """
        Generate a parameter value based on the provided schema and,
        if applicable, selected value.

        Parameters:
            param (Parameter): The schema.
            selected_value (Optional[Any]): The selected value for the parameter.

        Returns:
            Any : The generated parameter value.
        """
        return self.generate_random_value(
            param.schema.type, param.schema.enum, selected_value
        )

    def generate_parameters_dict(self, params: List[Parameter]) -> dict:
        """
        Generate a dictionary containing parameters based on the provided
        list of Property objects.

        Parameters:
            params (List[Parameter]): List of Property objects.

        Returns:
            dict: Dictionary containing generated parameters.
        """
        generated_params = {}

        for param in params:
            param_name = param.name
            param_value = self.generate_parameter(param)

            generated_params[param_name] = param_value

        return generated_params
