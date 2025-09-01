"""Tests for data classes."""
import pytest
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.uisp import UISPClientAddress
from classes.mikrotik import MikroTikClientAddress


class TestUISPClientAddress:
    """Test UISPClientAddress class."""

    def test_uisp_client_address_init(self):
        """Test UISPClientAddress initialization."""
        client = UISPClientAddress(
            ip_address="192.168.1.10",
            client_name="John Doe",
            client_id=1,
            service_id=101,
            service_status="active"
        )
        
        assert client.ip_address == "192.168.1.10"
        assert client.client_name == "John Doe"
        assert client.client_id == 1
        assert client.service_id == 101
        assert client.service_status == "active"

    def test_uisp_client_address_with_none_ip(self):
        """Test UISPClientAddress with None IP address."""
        client = UISPClientAddress(
            ip_address=None,
            client_name="John Doe",
            client_id=1,
            service_id=101,
            service_status="active"
        )
        
        assert client.ip_address is None
        assert client.client_name == "John Doe"

    def test_uisp_client_address_string_representation(self):
        """Test UISPClientAddress string representation."""
        client = UISPClientAddress(
            ip_address="192.168.1.10",
            client_name="John Doe",
            client_id=1,
            service_id=101,
            service_status="active"
        )
        
        # Test that the object can be converted to string (default repr)
        str_repr = str(client)
        assert "UISPClientAddress" in str_repr
        # Test that we can access the attributes
        assert client.ip_address == "192.168.1.10"
        assert client.client_name == "John Doe"


class TestMikroTikClientAddress:
    """Test MikroTikClientAddress class."""

    def test_mikrotik_client_address_init(self):
        """Test MikroTikClientAddress initialization."""
        address = MikroTikClientAddress(
            ip_address="192.168.1.10",
            list_name="clients_active",
            comment="John Doe",
            state="active",
            entry_id="1"
        )
        
        assert address.ip_address == "192.168.1.10"
        assert address.list_name == "clients_active"
        assert address.comment == "John Doe"
        assert address.state == "active"
        assert address.entry_id == "1"

    def test_mikrotik_client_address_with_empty_comment(self):
        """Test MikroTikClientAddress with empty comment."""
        address = MikroTikClientAddress(
            ip_address="192.168.1.10",
            list_name="clients_active",
            comment="",
            state="active",
            entry_id="1"
        )
        
        assert address.comment == ""

    def test_mikrotik_client_address_string_representation(self):
        """Test MikroTikClientAddress string representation."""
        address = MikroTikClientAddress(
            ip_address="192.168.1.10",
            list_name="clients_active",
            comment="John Doe",
            state="active",
            entry_id="1"
        )
        
        # Test that the object can be converted to string (default repr)
        str_repr = str(address)
        assert "MikroTikClientAddress" in str_repr
        # Test that we can access the attributes
        assert address.ip_address == "192.168.1.10"
        assert address.list_name == "clients_active"


class TestDataClassComparison:
    """Test comparison between data classes."""

    def test_uisp_and_mikrotik_address_comparison(self):
        """Test that UISP and MikroTik address objects can be compared by IP."""
        uisp_address = UISPClientAddress(
            ip_address="192.168.1.10",
            client_name="John Doe",
            client_id=1,
            service_id=101,
            service_status="active"
        )
        
        mikrotik_address = MikroTikClientAddress(
            ip_address="192.168.1.10",
            list_name="clients_active",
            comment="John Doe",
            state="active",
            entry_id="1"
        )
        
        # Both should have the same IP address
        assert uisp_address.ip_address == mikrotik_address.ip_address

    def test_address_objects_in_sets(self):
        """Test that address objects can be used in sets based on IP."""
        uisp_addresses = [
            UISPClientAddress("192.168.1.10", "John Doe", 1, 101, "active"),
            UISPClientAddress("192.168.1.20", "Jane Smith", 2, 102, "active"),
            UISPClientAddress("192.168.1.30", "Bob Johnson", 3, 103, "suspended")
        ]
        
        mikrotik_addresses = [
            MikroTikClientAddress("192.168.1.10", "clients_active", "John Doe", "active", "1"),
            MikroTikClientAddress("192.168.1.20", "clients_active", "Jane Smith", "active", "2")
        ]
        
        # Extract IP addresses for comparison
        uisp_ips = {addr.ip_address for addr in uisp_addresses if addr.ip_address is not None}
        mikrotik_ips = {addr.ip_address for addr in mikrotik_addresses if addr.ip_address is not None}
        
        # Should find missing IPs
        missing_ips = uisp_ips - mikrotik_ips
        assert "192.168.1.30" in missing_ips
