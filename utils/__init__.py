""" Utility functions for working with UISP and MikroTik RouterOS """

def strtobool(val: str) -> bool:
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"invalid truth value {val!r}")
import logging
import requests
import random

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


def str_to_bool(value):
    """Converts a string value to boolean."""
    return value.lower() in ["true", "yes", "1"]


def send_healthcheck_ping(check_url):
    try:
        response = requests.get(check_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        logger.info(f"Ping sent successfully!")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending ping: {e}")


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


def lookup_client_ip(devices, services, client_id, debug_mode=False):
    """Lookup a client IP address by client Id. Returns the IP if found, otherwise None."""
    if debug_mode:
        logger.debug(f"Looking up IP for client_id: {client_id}")
    
    # First, find the service for this client
    client_service = None
    for service in services:
        if service.get("clientId") == client_id:
            client_service = service
            if debug_mode:
                logger.debug(f"Found service for client {client_id}: {service}")
            break
    
    if not client_service:
        if debug_mode:
            logger.debug(f"No service found for client_id: {client_id}")
        return None
    
    if debug_mode:
        logger.debug(f"Service unmsClientSiteId: {client_service.get('unmsClientSiteId')}")
    
    # Now look for devices matching the site
    for device in devices:
        device_name = device.get("identification", {}).get("name", "Unknown device")
        if debug_mode:
            logger.debug(f"Checking device: {device_name}")
        
        # Log warning if device is missing identification or site data
        if not device.get("identification") or not device["identification"].get("site"):
            logger.warning(f"Device '{device_name}' (client ID: {client_id}) has no site assignment")
            continue

        device_site_id = device["identification"]["site"].get("id")
        if debug_mode:
            logger.debug(f"Device {device_name} site_id: {device_site_id}")
        
        if device_site_id == client_service["unmsClientSiteId"]:
            if debug_mode:
                logger.debug(f"Device {device_name} matches service site")
            if device.get("ipAddress"):
                ip = device.get("ipAddress").split("/")[0]
                if debug_mode:
                    logger.debug(f"Found IP for client {client_id}: {ip}")
                return ip
            else:
                logger.warning(f"Device '{device_name}' (client ID: {client_id}) has no IP address, using fallback")
                # TODO: Better handling of devices without an IP.
                _num = random.randint(2, 254)
                fallback_ip = f"192.0.0.{_num}"
                if debug_mode:
                    logger.debug(f"Using fallback IP for client {client_id}: {fallback_ip}")
                return fallback_ip
    
    if debug_mode:
        logger.debug(f"No matching device found for client_id: {client_id}")
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
