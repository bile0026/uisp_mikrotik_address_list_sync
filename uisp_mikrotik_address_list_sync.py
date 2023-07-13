import ipaddress
import netmiko

from __init__ import UISPMikroTikSyncConfig
from classes.uisp import UISPClientAddress
from classes.mikrotik import MikroTikClientAddress
from constants import (
    ucrm_api_version,
    uisp_api_version,
    all_list_name,
    suspended_list_name,
    active_list_name,
    service_status_map,
)
from utils.uisp import UISPApi, UCRMApi
from utils import lookup_client_ip, lookup_service_id, lookup_service_status

module_config = UISPMikroTikSyncConfig
client_list = [UISPClientAddress]
active_address_list = [MikroTikClientAddress]
suspended_address_list = [MikroTikClientAddress]

uisp_api = UISPApi(
    base_url=module_config.uisp_fqdn,
    token=module_config.uisp_api_token,
    api_version=uisp_api_version,
    verify=True,
)
ucrm_api = UCRMApi(
    base_url=module_config.uisp_fqdn,
    token=module_config.uisp_api_token,
    api_version=ucrm_api_version,
    verify=True,
)


def load_uisp_addresses():
    """Load IP addresses and client information from UISP."""

    clients = ucrm_api.get_clients()
    services = ucrm_api.get_services()
    devices = uisp_api.get_devices()

    for client in clients:
        _client_id = client["id"]
        _client_ip = lookup_client_ip(devices=devices, client_id=_client_id)
        _client_name = f'{client["firstName"]} {client["lastName"]}'
        _service_id = lookup_service_id(services=services, client_id=_client_id)
        _service_status = lookup_service_status(services=services, client_id=_client_id)

        new_client = UISPClientAddress(
            ip_address=_client_ip,
            client_name=_client_name,
            client_id=_client_id,
            service_id=_service_id,
            service_status=service_status_map[_service_status],
        )

        client_list.append(new_client)


def load_mikrotik_addresses():
    """Load IP addresses from MikroTik address lists."""

    pass


def sync_addresses():
    """Sync addresses from the UISP information to MikroTik address lists."""

    pass


if __name__ == "__main__":
    sync_addresses()
