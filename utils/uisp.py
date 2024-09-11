""" Utility Methods for working with UISP Clients """
from utils.base import ApiEndpoint
import logging

logger = logging.getLogger(__name__)


class UISPApi(ApiEndpoint):
    """interactions with the UISP Api"""

    def __init__(
        self,
        base_url: str,
        api_version: str,
        token: str,
        params: dict = {},
        verify: bool = True,
        use_ssl: bool = True,
    ):
        """Create UISP API connection."""
        super().__init__(base_url=base_url)
        self.base_url = "http://" + base_url + "/nms/" + "api/" + api_version + "/"
        if not use_ssl:
            self.base_url = "https://" + base_url + "/nms/" + "api/" + api_version + "/"
        self.api_version = api_version
        self.verify = verify
        self.params = params
        self.headers = {"x-auth-token": token, "Content-Type": "application/json"}
        self.token = token

    def get_devices(self):
        """get a list of devices in UISP."""
        url = "devices"
        devices = self.api_call(path=url)
        return devices

    def get_sites(self):
        """get a list of sites in UISP."""
        url = "sites"
        sites = self.api_call(path=url)
        return sites


class UCRMApi(ApiEndpoint):
    """interactions with the UCRM Api"""

    def __init__(
        self,
        base_url: str,
        api_version: str,
        token: str,
        params: dict = {},
        verify: bool = True,
        use_ssl: bool = True,
    ):
        """Create UISP API connection."""
        super().__init__(base_url=base_url)
        self.base_url = "https://" + base_url + "/crm/" + "api/" + api_version + "/"
        if not use_ssl:
            self.base_url = "http://" + base_url + "/crm/" + "api/" + api_version + "/"
        self.api_version = api_version
        self.headers = {"x-auth-app-key": token, "Content-Type": "application/json"}
        self.params = params
        self.verify = verify
        self.token = token

    def get_clients(self):
        """get a list of clients in UISP."""
        url = "clients"
        clients = self.api_call(path=url)
        return clients

    def get_services(self):
        """get a list of services in UISP."""
        url = "clients/services"
        services = self.api_call(path=url)
        return services
