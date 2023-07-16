"""Classes for uisp_mikrotik_address_list_sync"""

from . import ClientAddress
import logging

logger = logging.getLogger(__name__)


class MikroTikClientAddress(ClientAddress):
    """Object for storing information from UISP."""

    comment: str
    list_name: str
    state: str
    entry_id: str

    def __init__(self, ip_address, list_name, comment, state, entry_id):
        super().__init__(ip_address)
        self.list_name = list_name
        self.comment = comment
        self.state = state
        self.entry_id = entry_id
