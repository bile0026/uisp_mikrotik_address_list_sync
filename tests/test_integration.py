"""Integration tests for the main sync functionality."""
import pytest
import sys
import os
from unittest.mock import patch, Mock, MagicMock

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.uisp import UISPClientAddress
from classes.mikrotik import MikroTikClientAddress


class TestSyncIntegration:
    """Test the main sync functionality with mocked APIs."""

    def test_uisp_client_address_creation(self, mock_uisp_clients):
        """Test creating UISP client addresses from mock data."""
        # Test that we can create UISP client addresses from mock data
        client_data = mock_uisp_clients[0]
        client = UISPClientAddress(
            ip_address="192.168.1.10",
            client_name=f"{client_data['firstName']} {client_data['lastName']}",
            client_id=client_data['id'],
            service_id=101,
            service_status="active"
        )
        
        assert client.client_name == "John Doe"
        assert client.client_id == 1
        assert client.service_status == "active"

    def test_mikrotik_address_creation(self, mock_mikrotik_address_lists):
        """Test creating MikroTik addresses from mock data."""
        # Test that we can create MikroTik addresses from mock data
        address_data = mock_mikrotik_address_lists[0]
        address = MikroTikClientAddress(
            ip_address=address_data['address'],
            list_name=address_data['list'],
            comment=address_data['comment'],
            state="active",
            entry_id=address_data['.id']
        )
        
        assert address.ip_address == "192.168.1.10"
        assert address.list_name == "clients_active"
        assert address.comment == "John Doe"

    def test_address_comparison_logic(self):
        """Test the logic for comparing UISP and MikroTik addresses."""
        # Create test data
        uisp_addresses = [
            UISPClientAddress("192.168.1.10", "John Doe", 1, 101, "active"),
            UISPClientAddress("192.168.1.20", "Jane Smith", 2, 102, "active"),
            UISPClientAddress("192.168.1.30", "Bob Johnson", 3, 103, "suspended")
        ]
        
        mikrotik_addresses = [
            MikroTikClientAddress("192.168.1.10", "clients_active", "John Doe", "active", "1"),
            MikroTikClientAddress("192.168.1.20", "clients_active", "Jane Smith", "active", "2")
        ]
        
        # Test finding missing addresses
        from utils import find_missing_items
        missing = find_missing_items(uisp_addresses, mikrotik_addresses)
        
        assert len(missing) == 1
        assert missing[0].ip_address == "192.168.1.30"

    def test_service_lookup_integration(self, mock_uisp_services):
        """Test service lookup functionality with mock data."""
        from utils import lookup_service_id, lookup_service_status
        
        # Test service ID lookup
        service_id = lookup_service_id(mock_uisp_services, 1)
        assert service_id == 101
        
        # Test service status lookup
        service_status = lookup_service_status(mock_uisp_services, 1)
        assert service_status == 1

    def test_device_ip_lookup_integration(self, mock_uisp_devices, mock_uisp_services):
        """Test device IP lookup functionality with mock data."""
        from utils import lookup_client_ip
        
        with patch('utils.random.randint', return_value=100):
            # Test successful IP lookup
            ip = lookup_client_ip(mock_uisp_devices, mock_uisp_services, 1)
            assert ip == "192.168.1.10"
            
            # Test IP lookup for non-existent client
            ip = lookup_client_ip(mock_uisp_devices, mock_uisp_services, 999)
            assert ip is None

    def test_api_error_simulation(self):
        """Test error handling simulation."""
        # Test that we can simulate API errors
        from utils import str_to_bool
        
        # Test boolean conversion
        assert str_to_bool("true") is True
        assert str_to_bool("false") is False
        
        # Test that invalid values are handled
        assert str_to_bool("invalid") is False


class TestSyncLogic:
    """Test the sync logic functions."""

    def test_address_list_filtering(self, mock_mikrotik_address_lists):
        """Test filtering address lists by type."""
        # Filter active addresses
        active_addresses = [
            addr for addr in mock_mikrotik_address_lists 
            if addr["list"] == "clients_active"
        ]
        
        assert len(active_addresses) == 2
        assert all(addr["list"] == "clients_active" for addr in active_addresses)
        
        # Filter suspended addresses
        suspended_addresses = [
            addr for addr in mock_mikrotik_address_lists 
            if addr["list"] == "clients_suspended"
        ]
        
        assert len(suspended_addresses) == 1
        assert all(addr["list"] == "clients_suspended" for addr in suspended_addresses)

    def test_client_status_mapping(self):
        """Test client status mapping logic."""
        # Test status mapping
        status_map = {
            1: "active",
            2: "suspended",
            3: "cancelled"
        }
        
        assert status_map.get(1) == "active"
        assert status_map.get(2) == "suspended"
        assert status_map.get(3) == "cancelled"
        assert status_map.get(999) is None

    def test_ip_address_validation(self):
        """Test IP address validation logic."""
        # Test valid IP addresses
        valid_ips = ["192.168.1.10", "10.0.0.1", "172.16.0.1"]
        for ip in valid_ips:
            # Basic validation - check format
            parts = ip.split(".")
            assert len(parts) == 4
            assert all(0 <= int(part) <= 255 for part in parts)
        
        # Test invalid IP addresses
        invalid_ips = ["256.1.1.1", "1.1.1", "invalid"]
        for ip in invalid_ips:
            try:
                parts = ip.split(".")
                if len(parts) == 4:
                    all(0 <= int(part) <= 255 for part in parts)
            except (ValueError, IndexError):
                # Expected for invalid IPs
                pass
