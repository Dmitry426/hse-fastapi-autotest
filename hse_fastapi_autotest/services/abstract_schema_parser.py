__all__ = "AbstractOpenApiParser"

import abc
from abc import ABC
from typing import Dict, Union


class AbstractOpenApiParser(ABC):
    """Parse openapi json to a more convenient and usable representation """

    @abc.abstractmethod
    def parse_request_body(self, request_body: Dict) -> Union[Dict, None]:
        """Parse request body to extract props to test
        :param request_body: Openapi request body
        :return : Dict containing parsed request body format if one
        """

        raise NotImplemented

    @abc.abstractmethod
    def parse_params(self, params: Dict) -> Union[Dict, None]:
        """Get params from OpenAPI schema
        :param params : Openapi params
        :return : Dict containing parsed request  params if one
        """
        raise NotImplemented

    @abc.abstractmethod
    def parse_responses(self, responses: Dict) -> Union[Dict, None]:
        """Get params from OpenAPI schema
          :param responses: Openapi response
          :return : List containing parsed responses if one   """
        raise NotImplemented
