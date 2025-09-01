""" Utility Methods for working with MikroTik RouterOS Queues """

from utils.base import ApiEndpoint
import base64
import json
import logging

logger = logging.getLogger(__name__)


class MikroTikApi(ApiEndpoint):
    """interactions with the MikroTik API"""

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        params: dict = {},
        ssl_verify: bool = True,
        use_ssl: bool = True,
    ):
        """Create MikroTik API connection."""
        super().__init__(base_url=base_url)
        self.base_url = f"https://{base_url}/rest/"
        if not use_ssl:
            self.base_url = f"http://{base_url}/rest/"
        self.verify = ssl_verify
        self.username = username
        self.password = password
        credentials = f"{self.username}:{self.password}"
        authentication = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        self.params = params
        self.headers = {"Accept": "*/*", "Authorization": f"Basic {authentication}"}

    def get_address_list(self, list_name=None):
        """get address-list by name from router"""
        if list_name is None:
            url = "ip/firewall/address-list"
            address_list = self.api_call(path=url)
        else:
            url = f"ip/firewall/address-list?list={list_name}"
            address_list = self.api_call(path=url)
        return address_list

    def get_address_list_item_id(self, list_name, address):
        """Delete an address from an address-list."""
        url = f"ip/firewall/address-list?list={list_name}&address={address}"
        address_item = self.api_call(path=url)

        return address_item

    def add_address_to_list(self, ip_address, list_name, comment=""):
        """Add an IP Address to an address-list."""
        url = f"ip/firewall/address-list"
        _data = {"list": list_name, "comment": comment, "address": ip_address}
        _data = json.dumps(_data)
        self.api_call(path=url, payload=_data, method="PUT")

    def remove_address_from_list(self, entry_id):
        """Remove an IP Address from an address-list."""
        url = f"ip/firewall/address-list/{entry_id}"
        self.api_call(path=url, method="DELETE", accept_204=True)

    def bulk_add_addresses_to_list(self, addresses_data):
        """Add multiple IP addresses to an address-list using concurrent requests.
        
        Args:
            addresses_data (list): List of dictionaries containing:
                - ip_address: IP address to add
                - list_name: Name of the address list
                - comment: Optional comment for the address
        """
        if not addresses_data:
            logger.info("No addresses to add in bulk operation")
            return
        
        logger.info(f"Bulk adding {len(addresses_data)} addresses")
        
        # Group addresses by list_name for more efficient operations
        addresses_by_list = {}
        for addr_data in addresses_data:
            list_name = addr_data.get('list_name')
            if list_name not in addresses_by_list:
                addresses_by_list[list_name] = []
            addresses_by_list[list_name].append(addr_data)
        
        # Process each list separately
        for list_name, addresses in addresses_by_list.items():
            logger.info(f"Bulk adding {len(addresses)} addresses to list '{list_name}'")
            
            # Use concurrent requests for better performance
            import concurrent.futures
            import threading
            
            # Thread-local storage for session reuse
            thread_local = threading.local()
            
            def get_session():
                if not hasattr(thread_local, "session"):
                    import requests
                    thread_local.session = requests.Session()
                    thread_local.session.headers.update(self.headers)
                    thread_local.session.verify = self.verify
                return thread_local.session
            
            def add_single_address(addr_data):
                """Add a single address using the session."""
                try:
                    session = get_session()
                    url = f"{self.base_url}ip/firewall/address-list"
                    payload = {
                        "list": list_name,
                        "address": addr_data.get('ip_address'),
                        "comment": addr_data.get('comment', '')
                    }
                    
                    response = session.put(url, json=payload)
                    response.raise_for_status()
                    return True, addr_data.get('ip_address')
                except Exception as e:
                    return False, f"{addr_data.get('ip_address')}: {str(e)}"
            
            # Use ThreadPoolExecutor for concurrent requests
            success_count = 0
            error_count = 0
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Submit all tasks
                future_to_addr = {
                    executor.submit(add_single_address, addr_data): addr_data 
                    for addr_data in addresses
                }
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_addr):
                    success, result = future.result()
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        logger.error(f"Failed to add address: {result}")
            
            logger.info(f"Bulk add completed for '{list_name}': {success_count} successful, {error_count} failed")
            
            # If there were errors, log them but don't fail the entire operation
            if error_count > 0:
                logger.warning(f"Some addresses failed to add to '{list_name}': {error_count} errors")

    def bulk_remove_addresses_from_list(self, addresses_data):
        """Remove multiple IP addresses from address-lists using concurrent requests.
        
        Args:
            addresses_data (list): List of dictionaries containing:
                - entry_id: Entry ID to remove
                - ip_address: IP address (for logging)
                - list_name: Name of the address list (for logging)
        """
        if not addresses_data:
            logger.info("No addresses to remove in bulk operation")
            return
        
        logger.info(f"Bulk removing {len(addresses_data)} addresses")
        
        # Group by list_name for better organization
        addresses_by_list = {}
        for addr_data in addresses_data:
            list_name = addr_data.get('list_name', 'unknown')
            if list_name not in addresses_by_list:
                addresses_by_list[list_name] = []
            addresses_by_list[list_name].append(addr_data)
        
        # Process each list separately
        for list_name, addresses in addresses_by_list.items():
            logger.info(f"Bulk removing {len(addresses)} addresses from list '{list_name}'")
            
            # Use concurrent requests for better performance
            import concurrent.futures
            import threading
            
            # Thread-local storage for session reuse
            thread_local = threading.local()
            
            def get_session():
                if not hasattr(thread_local, "session"):
                    import requests
                    thread_local.session = requests.Session()
                    thread_local.session.headers.update(self.headers)
                    thread_local.session.verify = self.verify
                return thread_local.session
            
            def remove_single_address(addr_data):
                """Remove a single address using the session."""
                try:
                    session = get_session()
                    url = f"{self.base_url}ip/firewall/address-list/{addr_data.get('entry_id')}"
                    
                    response = session.delete(url)
                    response.raise_for_status()
                    return True, addr_data.get('ip_address')
                except Exception as e:
                    return False, f"{addr_data.get('ip_address')}: {str(e)}"
            
            # Use ThreadPoolExecutor for concurrent requests
            success_count = 0
            error_count = 0
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # Submit all tasks
                future_to_addr = {
                    executor.submit(remove_single_address, addr_data): addr_data 
                    for addr_data in addresses
                }
                
                # Collect results
                for future in concurrent.futures.as_completed(future_to_addr):
                    success, result = future.result()
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        logger.error(f"Failed to remove address: {result}")
            
            logger.info(f"Bulk remove completed for '{list_name}': {success_count} successful, {error_count} failed")
            
            # If there were errors, log them but don't fail the entire operation
            if error_count > 0:
                logger.warning(f"Some addresses failed to remove from '{list_name}': {error_count} errors")

    def bulk_sync_address_list(self, list_name, addresses_to_add, addresses_to_remove):
        """Perform bulk sync operation for a single address list.
        
        Args:
            list_name (str): Name of the address list to sync
            addresses_to_add (list): List of addresses to add
            addresses_to_remove (list): List of addresses to remove
        """
        logger.info(f"Starting bulk sync for list '{list_name}'")
        logger.info(f"Adding {len(addresses_to_add)} addresses, removing {len(addresses_to_remove)} addresses")
        
        # Perform bulk operations
        if addresses_to_remove:
            self.bulk_remove_addresses_from_list(addresses_to_remove)
        
        if addresses_to_add:
            self.bulk_add_addresses_to_list(addresses_to_add)
        
        logger.info(f"Completed bulk sync for list '{list_name}'")

    def get_address_list_bulk(self, list_names=None):
        """Get multiple address lists in a single API call.
        
        Args:
            list_names (list): List of address list names to retrieve. If None, gets all lists.
        
        Returns:
            dict: Dictionary with list names as keys and address lists as values
        """
        if list_names is None:
            # Get all address lists
            url = "ip/firewall/address-list"
            all_addresses = self.api_call(path=url)
            
            # Group by list name
            result = {}
            for addr in all_addresses:
                list_name = addr.get('list')
                if list_name not in result:
                    result[list_name] = []
                result[list_name].append(addr)
            
            return result
        else:
            # Get specific lists
            result = {}
            for list_name in list_names:
                url = f"ip/firewall/address-list?list={list_name}"
                addresses = self.api_call(path=url)
                result[list_name] = addresses
            
            return result

    def get_entry_ids_bulk(self, addresses_to_remove):
        """Get entry IDs for multiple addresses in bulk to reduce API calls.
        
        Args:
            addresses_to_remove (list): List of dictionaries containing:
                - ip_address: IP address to look up
                - list_name: Name of the address list
        
        Returns:
            list: List of dictionaries with entry_id added
        """
        if not addresses_to_remove:
            return []
        
        # Get all address lists in one call
        all_addresses = self.get_address_list_bulk()
        
        # Create a lookup dictionary for faster matching
        lookup = {}
        for list_name, addresses in all_addresses.items():
            for addr in addresses:
                key = f"{list_name}:{addr.get('address')}"
                lookup[key] = addr.get('.id')
        
        # Match addresses to entry IDs
        result = []
        for addr_data in addresses_to_remove:
            key = f"{addr_data['list_name']}:{addr_data['ip_address']}"
            entry_id = lookup.get(key)
            
            if entry_id:
                addr_data_with_id = addr_data.copy()
                addr_data_with_id['entry_id'] = entry_id
                result.append(addr_data_with_id)
            else:
                logger.warning(f"Entry ID not found for {addr_data['ip_address']} in {addr_data['list_name']}")
        
        return result
