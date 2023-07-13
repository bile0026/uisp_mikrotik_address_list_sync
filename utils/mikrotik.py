""" Utility Methods for working with MikroTik RouterOS Queues """

from utils.base import ApiEndpoint
import base64


class MikroTikApi(ApiEndpoint):
    """interactions with the MikroTik API"""

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        params: dict = {},
        ssl_verify: bool = True,
    ):
        """Create MikroTik API connection."""
        super().__init__(base_url=base_url)
        self.base_url = f"https://{base_url}/rest/"
        self.verify = ssl_verify
        self.username = username
        self.password = password
        credentials = f"{self.username}:{self.password}"
        authentication = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        self.params = params
        self.headers = {"Accept": "*/*", "Authorization": f"Basic {authentication}"}

    def get_address_list(self, list_name=None):
        """get address-list by name from router"""
        if list_name is None:
            url = "ip/firewall/address-list"
            address_list = self.api_call(path=url)
        else:
            url = f"ip/firewall/address-list?list={list_name}"
            address_list = self.api_call(path=url)
        return address_list

    def add_address_to_list(self, ip_address, list_name, comment=""):
        """add an ip address to an address-list."""
        url = f"ip/firewall/address-list/add"
        _data = {"list": list_name, "comment": comment, "address": ip_address}
        self.api_call(path=url, payload=_data)