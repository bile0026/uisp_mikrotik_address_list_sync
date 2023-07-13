"""Classes for uisp_mikrotik_address_list_sync"""

from ipaddress import ip_address


class ClientAddress:
    """Object for client addresses and descriptive information."""

    ip_address: ip_address

    def __init__(self, ip_address):
        self.ip_address = ip_address
