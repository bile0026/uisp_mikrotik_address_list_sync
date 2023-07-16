"""Classes for uisp_mikrotik_address_list_sync"""

from ipaddress import ip_address
import logging

logger = logging.getLogger(__name__)


class ClientAddress:
    """Object for client addresses and descriptive information."""

    ip_address: ip_address

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key '{key}' not found.")
