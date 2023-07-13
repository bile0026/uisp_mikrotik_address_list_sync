""" Utility functions for working with UISP and MikroTik RouterOS """

from distutils.util import strtobool


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(arg))


def lookup_service_id(services, client_id):
    for service in services:
        if service.get("clientId") == client_id:
            return service.get("id")
    return None


def lookup_service_status(services, client_id):
    for service in services:
        if service.get("clientId") == client_id:
            return service.get("status")
    return None


def lookup_client_ip(devices, services, client_id):
    for service in services:
        if service.get("clientId") == client_id:
            for device in devices:
                if device["identification"]["site"].get("id") == service["unmsClientSiteId"]:
                    return device.get("ipAddress").split('/')[0]
    return None
