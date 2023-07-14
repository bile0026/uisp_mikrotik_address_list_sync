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
    service_status_map_reverse,
)
from utils.uisp import UISPApi, UCRMApi
from utils.mikrotik import MikroTikApi
from utils import (
    lookup_client_ip,
    lookup_service_id,
    lookup_service_status,
    get_objects_by_key_value,
    find_missing_items,
)

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


def compare_addresses(list_type, uisp_ips, mikrotik_ips):
    """Compare what's loaded from UISP to what's on the MikroTik. Returns addresses missing from UISP or MikroTik."""

    uisp_addresses = get_objects_by_key_value(
        object_list=uisp_ips, key="service_status", value=list_type
    )

    addresses_missing_uisp = find_missing_items(
        objects1=mikrotik_ips, objects2=uisp_addresses
    )
    addresses_missing_mikrotik = find_missing_items(
        objects1=uisp_addresses, objects2=mikrotik_ips
    )

    return addresses_missing_uisp, addresses_missing_mikrotik


def compare_all_addresses(uisp_ips, mikrotik_ips):
    """Compare what's loaded from UISP to what's on the MikroTik. Returns addresses missing from UISP or MikroTik."""

    addresses_missing_uisp = find_missing_items(
        objects1=mikrotik_ips, objects2=uisp_ips
    )
    addresses_missing_mikrotik = find_missing_items(
        objects1=uisp_ips, objects2=mikrotik_ips
    )

    return addresses_missing_uisp, addresses_missing_mikrotik


def sync_addresses():
    """Sync addresses from the UISP information to MikroTik address lists."""

    uisp_addresses = load_uisp_addresses()
    print(f"\n\nUISP Addresses: {uisp_addresses}")

    (
        mikrotik_all_addresses,
        mikrotik_active_addresses,
        mikrotik_suspended_addresses,
    ) = load_mikrotik_addresses()
    print(
        f"\n\nMikroTik Active Addresses: {mikrotik_active_addresses}\nMikrotik Suspended Addresses: {mikrotik_suspended_addresses}\nMikrotik All Addresses: {mikrotik_all_addresses}"
    )

    (
        addresses_suspended_missing_uisp,
        addresses_suspended_missing_mikrotik,
    ) = compare_addresses(
        list_type="suspended",
        uisp_ips=uisp_addresses,
        mikrotik_ips=mikrotik_suspended_addresses,
    )
    print(
        f"\n\nSuspended missing from UISP: {addresses_suspended_missing_uisp}\nSuspended missing from MikroTik: {addresses_suspended_missing_mikrotik}"
    )

    (
        addresses_active_missing_uisp,
        addresses_active_missing_mikrotik,
    ) = compare_addresses(
        list_type="active",
        uisp_ips=uisp_addresses,
        mikrotik_ips=mikrotik_active_addresses,
    )
    print(
        f"\n\nActive missing from UISP: {addresses_active_missing_uisp}\Active missing from MikroTik: {addresses_active_missing_mikrotik}"
    )

    (
        addresses_all_missing_uisp,
        addresses_all_missing_mikrotik,
    ) = compare_all_addresses(
        uisp_ips=uisp_addresses,
        mikrotik_ips=mikrotik_all_addresses,
    )
    print(
        f"\n\nAll missing from UISP: {addresses_all_missing_uisp}\All missing from MikroTik: {addresses_all_missing_mikrotik}"
    )

    for item in addresses_suspended_missing_uisp:
        _entry_id = mikrotik_api.get_address_list_item_id(list_name=getattr(item, "list_name"), address=getattr(item, "ip_address"))[0][".id"]

        print(f'Removing {getattr(item, "ip_address")} from {getattr(item, "list_name")}')
        mikrotik_api.remove_address_from_list(entry_id=_entry_id)

if __name__ == "__main__":
    sync_addresses()
