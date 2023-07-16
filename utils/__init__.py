""" Utility functions for working with UISP and MikroTik RouterOS """

from distutils.util import strtobool
import logging

logger = logging.getLogger(__name__)


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
    """Lookup a service Id based on a client Id. Returns the service Id if found, otherwise None."""
    for service in services:
        if service.get("clientId") == client_id:
            return service.get("id")
    return None


def lookup_service_status(services, client_id):
    """Lookup the status value for a service plan based on the client id. Returns status as an integer."""
    for service in services:
        if service.get("clientId") == client_id:
            return service.get("status")
    return None


def lookup_client_ip(devices, services, client_id):
    """Lookup a client IP address by client Id. Returns the IP if found, otherwise None."""
    for service in services:
        if service.get("clientId") == client_id:
            for device in devices:
                if (
                    device["identification"]["site"].get("id")
                    == service["unmsClientSiteId"]
                ):
                    return device.get("ipAddress").split("/")[0]
    return None


def get_objects_by_key_value(object_list, key, value):
    """Returns a subset of objects in a list by searching the key for a specific value."""
    subset = []
    for obj in object_list:
        if hasattr(obj, key) and getattr(obj, key) == value:
            subset.append(obj)
    return subset


def find_missing_items(objects1, objects2):
    """Returns a list of objects that are missing from objects2 compared to objects1."""
    missing_items = []

    # Extract IP addresses from objects2
    ip_addresses2 = {
        obj.ip_address
        for obj in objects2
        if hasattr(obj, "ip_address") and getattr(obj, "ip_address") is not None
    }

    # Check objects1 against IP addresses in objects2
    for obj in objects1:
        if hasattr(obj, "ip_address") and getattr(obj, "ip_address") is not None:
            if obj.ip_address not in ip_addresses2:
                missing_items.append(obj)

    return missing_items
