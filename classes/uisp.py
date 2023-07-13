"""Classes for uisp_mikrotik_address_list_sync"""

from . import ClientAddress


class UISPClientAddress(ClientAddress):
    """Object for storing information from UISP."""

    client_name: str
    client_id: int
    service_id: int
    service_status: str

    def __init__(self, ip_address, client_name, client_id, service_id, service_status):
        super().__init__(ip_address)
        self.client_name = client_name
        self.client_id = client_id
        self.service_id = service_id
        self.service_status = service_status
