"""Classes for uisp_mikrotik_address_list_sync"""

from . import ClientAddress


class UISPClientAddress(ClientAddress):
    """Object for storing information from UISP."""

    client_name: str
    client_id: int
    service_id: int
    service_status: str
