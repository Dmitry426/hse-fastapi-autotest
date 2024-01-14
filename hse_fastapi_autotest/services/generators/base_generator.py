import random
from abc import ABC
from typing import Any, List, Optional

from openapi_parser.enumeration import DataType


class AbstractBaseGenerator(ABC):
    def generate_random_value(
        self,
        data_type: DataType,
        enum_values: List[Any] = None,
        selected_value: Optional[Any] = None,
    ):
        """
        Generate a random value based on the provided data type and enum values.

        Parameters:
            data_type (str): The data type (e.g., 'string', 'integer', 'boolean', etc.).
            enum_values (List[Any]): Enum values if the parameter has an enum.
            selected_value (Optional[Any]): The selected value for the parameter.

        Returns:
            Any : The randomly generated value.
        """
        raise NotImplementedError


class BaseGenerator(AbstractBaseGenerator):
    def generate_random_value(
        self,
        data_type: DataType,
        enum_values: List[Any] = None,
        selected_value: Optional[Any] = None,
    ) -> Any:
        if selected_value is not None:
            return selected_value
        elif enum_values:
            return random.choice(enum_values)
        elif data_type == DataType.INTEGER:
            return random.randint(1, 5)
        elif data_type == DataType.NUMBER:
            return round(random.uniform(1, 5), 2)
        elif data_type == DataType.STRING:
            return self._generate_random_string()
        elif data_type == DataType.BOOLEAN:
            return random.choice([True, False])
        elif data_type == DataType.ARRAY:
            # For simplicity, return an empty list for array type
            return []
        elif data_type == DataType.OBJECT:
            # For simplicity, return an empty dictionary for object type
            return {}
        else:
            return None

    @staticmethod
    def _generate_random_string() -> str:
        """
        Generate a random string of the specified length.

        Returns:
            str: The randomly generated string.
        """
        return "name"
