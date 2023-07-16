""" Shared functions and classes """

from __init__ import UISPMikroTikSyncConfig
import requests
import urllib3
import json
from os.path import exists
from requests.auth import HTTPBasicAuth
from utils import is_truthy
import logging

logger = logging.getLogger(__name__)

module_config = UISPMikroTikSyncConfig

if module_config.disable_ssl_warning:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiEndpoint:
    """Base class to represent interactions with an API endpoint."""

    class Meta:
        """Meta data for ApiEndpoint class."""

        abstract = True

    def __init__(
        self,
        base_url: str,
        headers: dict = {},
        data: dict = {},
        ssl_verify: bool = True,
        accept_204: bool = False,
    ):
        """Create API connection."""
        self.base_url = base_url
        self.verify = ssl_verify
        self.headers = {"Accept": "*/*", "Content-Type": "application/json"}
        self.data = data
        self.accept_204 = False

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def validate_url(self, path):
        """Validate URL formatting is correct.
        Args:
            path (str): URI path for API endpoint
        Returns:
            str: Formatted URL path for API endpoint
        """
        if not self.base_url.endswith("/") and not path.startswith("/"):
            full_path = f"{self.base_url}/{path}"
        else:
            full_path = f"{self.base_url}{path}"
        if not full_path.endswith("/"):
            return full_path
        return full_path

    def api_call(
        self,
        path: str,
        method: str = "GET",
        params: dict = {},
        payload: dict = {},
        accept_204: bool = False,
    ):  # pylint: disable=dangerous-default-value
        """Send Request to API endpoint of type `method`. Defaults to GET request.
        Args:
            path (str): API path to send request to.
            method (str, optional): API request method. Defaults to "GET".
            params (dict, optional): Additional parameters to send to API. Defaults to None.
            payload (dict, optional): Message payload to be sent as part of API call.
        Raises:
            Exception: Error thrown if request errors.
        Returns:
            dict: JSON payload of API response.
        """
        url = self.validate_url(path)

        if not params:
            params = self.params
        else:
            params = {**self.params, **params}

        response = requests.request(
            method=method,
            headers=self.headers,
            url=url,
            params=params,
            verify=is_truthy(self.verify),
            data=payload,
        )
        try:
            logger.debug(f"API Response: {response}")
            response.raise_for_status()
            if response.status_code == 204 and not accept_204:
                return None
            elif response.text:  # Check if the response is not empty
                return response.json()
            else:
                return None
        except requests.exceptions.HTTPError as err:
            logger.error(f"Error communicating to the API: {err}")
            raise Exception(f"Error communicating to the API: {err}")
        except json.JSONDecodeError as err:
            logger.error(f"Error decoding API response as JSON: {err}")
            raise Exception(f"Error decoding API response as JSON: {err}")
