"""Classes for uisp_mikrotik_address_list_sync"""

from . import ClientAddress


class MikroTikClientAddress(ClientAddress):
    """Object for storing information from UISP."""

    comment: str
    list_name: str
