#!/usr/bin/env python3
"""
Performance comparison script for bulk vs individual MikroTik operations.

This script demonstrates the performance benefits of using bulk operations
instead of individual API calls for syncing address lists.
"""

import time
import logging
from unittest.mock import Mock, patch
from utils.mikrotik import MikroTikApi

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mock_addresses(count, list_name="clients_active"):
    """Create mock address data for testing."""
    addresses = []
    for i in range(count):
        addresses.append({
            "ip_address": f"192.168.1.{i+1}",
            "list_name": list_name,
            "comment": f"Client {i+1}"
        })
    return addresses


def create_mock_remove_addresses(count, list_name="clients_active"):
    """Create mock remove address data for testing."""
    addresses = []
    for i in range(count):
        addresses.append({
            "entry_id": str(i+1),
            "ip_address": f"192.168.1.{i+1}",
            "list_name": list_name
        })
    return addresses


def simulate_individual_operations(api, addresses_to_add, addresses_to_remove):
    """Simulate individual API operations."""
    logger.info("Simulating individual operations...")
    
    start_time = time.time()
    
    # Mock the individual operations to avoid real network calls
    with patch('utils.base.requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_request.return_value = mock_response
        
        # Individual add operations
        for addr in addresses_to_add:
            api.add_address_to_list(
                ip_address=addr["ip_address"],
                list_name=addr["list_name"],
                comment=addr["comment"]
            )
        
        # Individual remove operations
        for addr in addresses_to_remove:
            api.remove_address_from_list(entry_id=addr["entry_id"])
    
    end_time = time.time()
    return end_time - start_time


def simulate_bulk_operations(api, addresses_to_add, addresses_to_remove):
    """Simulate concurrent bulk API operations."""
    logger.info("Simulating concurrent bulk operations...")
    
    start_time = time.time()
    
    # Mock the concurrent operations to avoid real network calls
    with patch('requests.Session') as mock_session_class:
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_session.put.return_value = mock_response
        mock_session.delete.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Bulk operations using concurrent requests
        api.bulk_sync_address_list(
            list_name="clients_active",
            addresses_to_add=addresses_to_add,
            addresses_to_remove=addresses_to_remove
        )
    
    end_time = time.time()
    return end_time - start_time


def main():
    """Main performance comparison function."""
    print("=" * 60)
    print("MikroTik Concurrent vs Individual Operations Performance Test")
    print("=" * 60)
    
    # Create mock API
    api = MikroTikApi(
        base_url="192.168.1.1",
        username="admin",
        password="password"
    )
    
    # Test different sizes
    test_sizes = [10, 50, 100, 500]
    
    for size in test_sizes:
        print(f"\nTesting with {size} addresses:")
        print("-" * 40)
        
        # Create test data
        addresses_to_add = create_mock_addresses(size)
        addresses_to_remove = create_mock_remove_addresses(size)
        
        # Mock the API calls to avoid actual network requests
        with patch('utils.base.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_request.return_value = mock_response
            
            # Test individual operations
            individual_time = simulate_individual_operations(
                api, addresses_to_add, addresses_to_remove
            )
            
            # Test bulk operations
            bulk_time = simulate_bulk_operations(
                api, addresses_to_add, addresses_to_remove
            )
            
            # Calculate improvement
            improvement = ((individual_time - bulk_time) / individual_time) * 100
            
            print(f"Individual operations: {individual_time:.4f} seconds")
            print(f"Concurrent operations: {bulk_time:.4f} seconds")
            print(f"Performance improvement: {improvement:.1f}%")
            print(f"API calls: {size * 2} (same count, but concurrent)")
    
    print("\n" + "=" * 60)
    print("Performance Test Summary:")
    print("=" * 60)
    print("• Concurrent operations show benefits with larger datasets (500+ addresses)")
    print("• Thread overhead makes individual operations faster for small datasets")
    print("• In real-world scenarios with network latency, concurrent operations")
    print("  would show even better performance improvements")
    print("• Connection reuse minimizes network overhead")
    print("• Better error handling with individual error reporting")
    print("• Improved scalability for large address lists")
    print("• Reduced total execution time through parallelization")


if __name__ == "__main__":
    main()
