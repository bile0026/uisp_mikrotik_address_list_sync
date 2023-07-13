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
from utils.mikrotik import MikroTikApi
from utils import lookup_client_ip, lookup_service_id, lookup_service_status

module_config = UISPMikroTikSyncConfig
client_list = [UISPClientAddress]
active_address_list = [MikroTikClientAddress]
suspended_address_list = [MikroTikClientAddress]
all_address_list = [MikroTikClientAddress]

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

mikrotik_api = MikroTikApi(
    base_url=module_config.mt_ip,
    username=module_config.mt_username,
    password=module_config.mt_password,
    ssl_verify=module_config.ssl_verify,
)


def load_uisp_addresses():
    """Load IP addresses and client information from UISP."""

    clients = ucrm_api.get_clients()
    services = ucrm_api.get_services()
    devices = uisp_api.get_devices()

    for client in clients:
        _client_id = client["id"]
        _client_ip = lookup_client_ip(
            devices=devices, services=services, client_id=_client_id
        )
        _client_name = f'{client["firstName"]} {client["lastName"]}'
        _service_id = lookup_service_id(services=services, client_id=_client_id)
        _service_status = lookup_service_status(services=services, client_id=_client_id)

        new_client = UISPClientAddress(
            ip_address=_client_ip,
            client_name=_client_name,
            client_id=_client_id,
            service_id=_service_id,
            service_status=service_status_map.get(_service_status),
        )

        client_list.append(new_client)

    return client_list


def load_mikrotik_addresses():
    """Load IP addresses from MikroTik address lists."""
    active_addresses = []
    suspended_addresses = []
    all_addresses = []

    active_address_list = mikrotik_api.get_address_list(list_name=active_list_name)
    suspended_address_list = mikrotik_api.get_address_list(
        list_name=suspended_list_name
    )
    all_address_list = mikrotik_api.get_address_list(list_name=all_list_name)

    for address in active_address_list:
        try:
            _comment = address["comment"]
        except TypeError:
            _comment = ""
        except KeyError:
            _comment = ""

        new_address = MikroTikClientAddress(
            ip_address=address["address"],
            list_name=address["list"],
            comment=_comment,
            state="active",
            entry_id=address[".id"],
        )

        active_addresses.append(new_address)

    for address in suspended_address_list:
        try:
            _comment = address["comment"]
        except TypeError:
            _comment = ""
        except KeyError:
            _comment = ""

        new_address = MikroTikClientAddress(
            ip_address=address["address"],
            list_name=address["list"],
            comment=_comment,
            state="suspended",
            entry_id=address[".id"],
        )

        suspended_addresses.append(new_address)

    for address in all_address_list:
        try:
            _comment = address["comment"]
        except TypeError:
            _comment = ""
        except KeyError:
            _comment = ""

        new_address = MikroTikClientAddress(
            ip_address=address["address"],
            list_name=address["list"],
            comment=_comment,
            state="None",
            entry_id=address[".id"],
        )

        all_addresses.append(new_address)

    return all_addresses, active_addresses, suspended_addresses


def sync_addresses():
    """Sync addresses from the UISP information to MikroTik address lists."""

    uisp_addresses = load_uisp_addresses()
    print(f"UISP Addresses: {uisp_addresses}")

    (
        mikrotik_all_addresses,
        mikrotik_active_addresses,
        mikrotik_suspended_addresses,
    ) = load_mikrotik_addresses()
    print(
        f"MikroTik Active Addresses: {mikrotik_active_addresses}\nMikrotik Suspended Addresses: {mikrotik_suspended_addresses}\nMikrotik All Addresses: {mikrotik_all_addresses}"
    )


if __name__ == "__main__":
    sync_addresses()
